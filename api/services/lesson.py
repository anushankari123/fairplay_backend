from uuid import UUID
from api.db.models.lesson import Lesson
from api.interfaces.lesson import LessonRead, LessonCreate, LessonUpdate
from api.interfaces.utils import List
from api.utils.exceptions import NotFoundError
from .base import BaseService


class LessonService(BaseService):
    async def get_lesson(self, lesson_id: UUID) -> LessonRead:
        res = await Lesson.get(self.db, filters=[Lesson.id == lesson_id])
        lesson = res.one_or_none()
        if not lesson:
            raise NotFoundError("Lesson not found")
        return lesson

    async def create_lesson(self, data: LessonCreate) -> LessonRead:
        new_lesson = Lesson(**data.model_dump())
        await new_lesson.save(self.db)
        return new_lesson

    async def delete_lesson(self, lesson_id: UUID):
        lesson = await self.get_lesson(lesson_id)
        lesson.is_deleted = True
        await lesson.save(self.db)

    async def get_lessons(self) -> List[LessonRead]:
        """
        Retrieve a list of non-deleted modules.

        Returns:
        - List[ModuleRead]: List of non-deleted modules.
        """
        res = await Lesson.get(self.db, filters=[~Lesson.is_deleted])  # Fetch modules where is_deleted is False
        return {"data": res.all()}
    
    async def set_lesson_quiz_score(self, user_id: UUID, module_id: UUID, lesson_id: UUID, quiz_score: int) -> LessonRead:
        lesson = await self.get_lesson(lesson_id)
        if lesson.user_id != user_id:
            raise NotFoundError("Lesson does not belong to this user")
        lesson.lesson_quiz = quiz_score
        await lesson.save(self.db)
        return lesson

    # Get the quiz score for a user, module, and lesson
    async def get_lesson_quiz_score_for_user(self, module_id: UUID, lesson_id: UUID, user_id: UUID) -> Lesson:
        res = await Lesson.get(self.db, filters=[Lesson.user_id == user_id, Lesson.module_id == module_id, Lesson.id == lesson_id, ~Lesson.is_deleted])
        lesson = res.one_or_none()
        if not lesson:
            raise NotFoundError(f"Lesson with ID {lesson_id} in module {module_id} for user {user_id} not found")
        return lesson

    # Increment lesson progress (lesson completed)
    async def increment_lesson_progress(self, user_id: UUID, module_id: UUID, lesson_id: UUID, lesson_completed: bool = False) -> Lesson:
        res = await Lesson.get(self.db, filters=[Lesson.user_id == user_id, Lesson.module_id == module_id, Lesson.id == lesson_id, ~Lesson.is_deleted])
        lesson = res.one_or_none()
        if not lesson:
            raise NotFoundError(f"Lesson with ID {lesson_id} in module {module_id} for user {user_id} not found")
        
        if lesson_completed:
            lesson.lessons_completed += 1
        
        await lesson.save(self.db)
        return lesson

