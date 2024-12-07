from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.sql import not_
from typing import Optional

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import blue
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os
from datetime import datetime, timezone

from sqlmodel import col

from api.db.models.certificate import Certificate
from api.db.models.module import ModuleQuiz
from api.db.models.user import User
from api.interfaces.certificate import CertificateCreate
from api.utils.exceptions import NotFoundError
from .base import BaseService

class CertificateService(BaseService):
  
    async def create_certificate(self, data: CertificateCreate) -> Certificate:
        """
        Create a new certificate for a completed module.
        
        Args:
        - data (CertificateCreate): Information to create the certificate.
        
        Returns:
        - Certificate: Details of the created certificate.
        """
        # Verify module quiz exists and is completed
        module_quiz = await ModuleQuiz.get(
            db=self.db,
            filters=[
                ModuleQuiz.id == data.module_quiz_id, 
                ModuleQuiz.module_completed >= 1, 
                ~col(ModuleQuiz.is_deleted)
            ]
        )
        module_quiz = module_quiz.one_or_none()

        if not module_quiz:
            raise NotFoundError("Module quiz not completed or does not exist")
        
        # Verify user exists
        user = await User.get(
            db=self.db, 
            filters=[User.id == data.user_id, ~col(User.is_deleted)]
        )
        user = user.one_or_none()

        if not user:
            raise NotFoundError("User not found")
        
        # Check if certificate already exists
        existing_certificate = await self.get_certificate_by_module_quiz(data.module_quiz_id)
        if existing_certificate:
            return existing_certificate
        
        # Generate certificate PDF
        certificate_url = await self.generate_certificate_pdf(
            user, 
            data.module_name or module_quiz.module_name, 
            data.score or module_quiz.m_quizscore
        )
        
        # Ensure created_at and updated_at are timezone-aware
        now = datetime.now(timezone.utc)
        
        # Create certificate record
        certificate_data = {
            'user_id': data.user_id,
            'module_quiz_id': data.module_quiz_id,
            'module_name': data.module_name or module_quiz.module_name,
            'score': data.score or module_quiz.m_quizscore,
            'certificate_url': certificate_url,
            'created_at': now,
            'updated_at': now
        }
        
        new_certificate = Certificate(**certificate_data)
        await new_certificate.save(self.db)
        return new_certificate

    async def generate_certificate_pdf(self, user: User, module_name: str, score: int) -> str:
        """
        Generate a PDF certificate.
        
        Args:
        - user (User): User who completed the module
        - module_name (str): Name of the completed module
        - score (int): Score achieved
        
        Returns:
        - str: Path to the generated certificate PDF
        """
        # Ensure certificates directory exists
        os.makedirs('certificates', exist_ok=True)
        
        # Generate unique filename
        filename = f'certificates/{user.id}_{module_name}_{datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")}.pdf'
        
        # Create PDF
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Background
        c.setFillColor(blue)
        c.rect(50, 50, width-100, height-100, stroke=1, fill=0)
        
        # Title
        c.setFont('Helvetica-Bold', 24)
        c.drawCentredString(width / 2, height - 150, "Certificate of Completion")
        
        # User Details
        c.setFont('Helvetica', 16)
        c.drawCentredString(width / 2, height - 200, f"This is to certify that")
        
        c.setFont('Helvetica-Bold', 20)
        full_name = f"{user.first_name} {user.last_name}".strip()
        c.drawCentredString(width / 2, height - 230, full_name)
        
        # Module Details
        c.setFont('Helvetica', 16)
        c.drawCentredString(width / 2, height - 260, f"has successfully completed the module")
        
        c.setFont('Helvetica-Bold', 18)
        c.drawCentredString(width / 2, height - 290, module_name)
        
        # Score
        c.setFont('Helvetica', 14)
        c.drawCentredString(width / 2, height - 320, f"with a score of {score}")
        
        # Date
        c.setFont('Helvetica', 12)
        c.drawCentredString(width / 2, height - 400, f"Dated: {datetime.now(timezone.utc).strftime('%B %d, %Y')}")
        
        c.showPage()
        c.save()
        
        return filename

    async def get_certificates_by_user(self, user_id: UUID):
        """
        Retrieve all certificates for a specific user.
        """
        query = select(Certificate).where(
            Certificate.user_id == user_id,
            not_(Certificate.is_deleted)
        )
        
        result = await self.db.execute(query)
        return {"data": result.scalars().all()}
    async def get_certificate_by_module_quiz(self, module_quiz_id: UUID) -> Optional[Certificate]:
        """
        Retrieve a certificate by module quiz ID.
        """
        query = select(Certificate).where(
            Certificate.module_quiz_id == module_quiz_id,
            not_(Certificate.is_deleted)
        )
        
        result = await self.db.execute(query)
        return result.scalars().one_or_none()
