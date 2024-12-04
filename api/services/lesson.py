from uuid import UUID
from sqlmodel import col
from api.db.models.lesson import LessonQuiz
from api.interfaces.lesson import LessonQuizCreate
from sqlalchemy.future import select
from sqlalchemy.sql import not_
from api.interfaces.utils import List
from api.utils.exceptions import NotFoundError
from .base import BaseService

class LessonQuizService(BaseService):
    async def get_lesson_quizzes_by_user(self, user_id: UUID) -> List[LessonQuiz]:
        """
        Retrieve lesson quizzes for a specific user.
        """
        res = await LessonQuiz.get(
            db=self.db,
            filters=[LessonQuiz.user_id == user_id, ~col(LessonQuiz.is_deleted)]
        )
        return {"data": res.all()}

    async def get_lesson_quiz_by_id(self, lesson_quiz_id: UUID) -> LessonQuiz:
        """
        Retrieve a specific lesson quiz by its ID.
        """
        res = await LessonQuiz.get(db=self.db, filters=[LessonQuiz.id == lesson_quiz_id, ~col(LessonQuiz.is_deleted)])
        lesson_quiz = res.one_or_none()
        if lesson_quiz is None:
            raise NotFoundError("Lesson quiz not found")
        return lesson_quiz

    async def update_lesson_quiz_score(self, lesson_quiz_id: UUID, score: int) -> LessonQuiz:
        """
        Update lesson quiz score conditionally.
        """
        lesson_quiz = await self.get_lesson_quiz_by_id(lesson_quiz_id)
        
        if lesson_quiz.l_quizscore == 0:
            lesson_quiz.l_quizscore = score
        elif score > lesson_quiz.l_quizscore:
            lesson_quiz.l_quizscore = score
        
        await lesson_quiz.save(self.db)
        return lesson_quiz
    
    async def create_lesson_quiz(self, data: LessonQuizCreate) -> LessonQuiz:
        """
        Create a new module quiz or fetch an existing one if a combination of
        `user_id` and `module_name` already exists.

        Args:
        - data (ModuleQuizCreate): Information to create the module quiz.

        Returns:
        - ModuleQuiz: Details of the created or fetched module quiz.
        """
        # Check if the combination of `user_id` and `module_name` exists
        query = select(LessonQuiz).where(
        LessonQuiz.user_id == data.user_id,
        LessonQuiz.lesson_name == data.lesson_name,
        not_(LessonQuiz.is_deleted)
        )

        result = await self.db.execute(query)
        existing_quiz = result.scalars().one_or_none()

        if existing_quiz:
            # If the combination exists, return the existing data
            return existing_quiz

        # If the combination does not exist, create a new record
        new_module_quiz = LessonQuiz(**data.model_dump())
        await new_module_quiz.save(self.db)
        return new_module_quiz

    async def delete_lesson_quiz(self, lesson_quiz_id: UUID):
        """
        Mark a module quiz as deleted.
        """
        module_quiz = await self.get_lesson_quiz_by_id(lesson_quiz_id)
        module_quiz.is_deleted = True
        await module_quiz.save(self.db)