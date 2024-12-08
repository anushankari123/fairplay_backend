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
            data (CertificateCreate): Data for certificate creation

        Returns:
            Certificate: The newly created certificate
        """
        try:
            # Fetch the corresponding module quiz to get the latest score
            query = select(ModuleQuiz).where(
                ModuleQuiz.id == data.module_quiz_id,
                ~col(ModuleQuiz.is_deleted)
            )
            result = await self.db.execute(query)
            module_quiz = result.scalars().one_or_none()
            
            if module_quiz:
                # Override the score with the module quiz's actual score
                data.score = module_quiz.m_quizscore
            else:
                # If no module quiz found, log and potentially raise an exception
                print(f"No module quiz found for ID: {data.module_quiz_id}")
                raise NotFoundError("Associated module quiz not found")
            
            # Check if a certificate already exists for this module quiz
            existing_certificate_query = select(Certificate).where(
                Certificate.module_quiz_id == data.module_quiz_id,
                ~col(Certificate.is_deleted)
            )
            existing_certificate_result = await self.db.execute(existing_certificate_query)
            existing_certificate = existing_certificate_result.scalars().one_or_none()
            
            if existing_certificate:
                # If certificate exists, update the existing one
                existing_certificate.score = data.score
                await existing_certificate.save(self.db)
                return existing_certificate
            
            # Create a new certificate
            new_certificate = Certificate(**data.model_dump())
            
            # Optional: Generate a certificate URL if needed
            # This could be a method to generate a unique certificate URL
           
            
            await new_certificate.save(self.db)
            return new_certificate
        
        except Exception as e:
            # Log the full error for debugging
            print(f"Error creating certificate: {e}")
            # Optionally re-raise the exception or handle it as needed
            raise

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