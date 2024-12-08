from datetime import datetime
from uuid import UUID
from fastapi import HTTPException
from sqlmodel import col
from sqlalchemy.future import select
from sqlalchemy.sql import not_

from api.interfaces.utils import List
from api.interfaces.module import ModuleQuizCreate
from api.utils.exceptions import NotFoundError

from api.services.certificate import CertificateService
from api.interfaces.certificate import CertificateCreate
from api.db.models.module import ModuleQuiz
from .base import BaseService

class ModuleQuizService(BaseService):
    async def get_module_quizzes_by_user(self, user_id: UUID) -> List[ModuleQuiz]:
        """
        Retrieve module quizzes for a specific user.
        """
        res = await ModuleQuiz.get(
            db=self.db,
            filters=[ModuleQuiz.user_id == user_id, ~col(ModuleQuiz.is_deleted)]
        )
        return {"data": res.all()}

    async def get_module_quiz_by_id(self, module_quiz_id: UUID) -> ModuleQuiz:
        """
        Retrieve a specific module quiz by its ID.
        """
        res = await ModuleQuiz.get(db=self.db, filters=[ModuleQuiz.id == module_quiz_id, ~col(ModuleQuiz.is_deleted)])
        module_quiz = res.one_or_none()
        if module_quiz is None:
            raise NotFoundError("Module quiz not found")
        return module_quiz

    async def increment_module_progress(self, module_quiz_id: UUID) -> ModuleQuiz:
        """
        Increment module progress by one. If progress is already noted, return the existing data without incrementing.
        """
        module_quiz = await self.get_module_quiz_by_id(module_quiz_id)
        if module_quiz.module_progress >= 1:
            # Return the existing data without incrementing
            return module_quiz
        
        module_quiz.module_progress += 1
        await module_quiz.save(self.db)
        return module_quiz

    async def increment_module_completed(self, module_quiz_id: UUID) -> ModuleQuiz:
        try:
            module_quiz = await self.get_module_quiz_by_id(module_quiz_id)

            if module_quiz.module_completed >= 1:
                return module_quiz

            module_quiz.module_completed += 1
            
            module_quiz.completed_at = datetime.now()
            await module_quiz.save(self.db)
            
            # Refresh to ensure latest data
            await self.db.refresh(module_quiz)

            # Certificate creation logic remains the same
            certificate_service = CertificateService(db=self.db)
            existing_certificate = await certificate_service.get_certificate_by_module_quiz(module_quiz_id)

            if not existing_certificate:
                certificate_data = CertificateCreate(
                    module_quiz_id=module_quiz_id,
                    user_id=module_quiz.user_id,
                    module_name=module_quiz.module_name,
                    score=module_quiz.m_quizscore
                )
                await certificate_service.create_certificate(certificate_data)

            return module_quiz
        except NotFoundError as nfe:
            # Specific handling for not found errors
            raise HTTPException(status_code=404, detail=str(nfe))
        except Exception as e:
            # More detailed logging and specific error handling
            print(f"Detailed error in increment_module_completed: {e}")
            raise HTTPException(status_code=500, detail="Failed to complete module")



    async def update_module_quiz_score(self, module_quiz_id: UUID, score: int) -> ModuleQuiz:
        """
        Update module quiz score conditionally.
        """
        module_quiz = await self.get_module_quiz_by_id(module_quiz_id)
        
        if module_quiz.m_quizscore == 0:
            module_quiz.m_quizscore = score
        elif score > module_quiz.m_quizscore:
            module_quiz.m_quizscore = score
        
        await module_quiz.save(self.db)
        return module_quiz
    
    async def create_module_quiz(self, data: ModuleQuizCreate) -> ModuleQuiz:
        """
        Create a new module quiz or fetch an existing one if a combination of
        `user_id` and `module_name` already exists.

        Args:
        - data (ModuleQuizCreate): Information to create the module quiz.

        Returns:
        - ModuleQuiz: Details of the created or fetched module quiz.
        """
        # Check if the combination of `user_id` and `module_name` exists
        query = select(ModuleQuiz).where(
        ModuleQuiz.user_id == data.user_id,
        ModuleQuiz.module_name == data.module_name,
        not_(ModuleQuiz.is_deleted)
        )

        result = await self.db.execute(query)
        existing_quiz = result.scalars().one_or_none()

        if existing_quiz:
            # If the combination exists, return the existing data
            return existing_quiz

        # If the combination does not exist, create a new record
        new_module_quiz = ModuleQuiz(**data.model_dump())
        await new_module_quiz.save(self.db)
        return new_module_quiz

    async def delete_module_quiz(self, module_quiz_id: UUID):
        """
        Mark a module quiz as deleted.
        """
        module_quiz = await self.get_module_quiz_by_id(module_quiz_id)
        module_quiz.is_deleted = True
        await module_quiz.save(self.db)

    async def get_total_progress_and_completed(self, user_id: UUID) -> dict:
        """
        Get the total progress and total completed for a specific user.
        """
        try:
            query = select(ModuleQuiz).where(
                ModuleQuiz.user_id == user_id,
                not_(ModuleQuiz.is_deleted)
            )

            result = await self.db.execute(query)
            quizzes = result.scalars().all()

            # Aggregate progress and completed counts
            total_progress = sum(quiz.module_progress for quiz in quizzes)
            total_completed = sum(quiz.module_completed for quiz in quizzes)

            return {
                "total_progress": total_progress,
                "total_completed": total_completed
            }
        except Exception as e:
            # Add more detailed logging
            print(f"Error in get_total_progress_and_completed: {e}")
            raise