from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import LessonService
from api.interfaces.utils import List
from api.interfaces.lesson import LessonRead, LessonCreate, LessonUpdate

lesson_router = APIRouter(prefix="/lessons")


@lesson_router.get("/{lesson_id}", response_model=LessonRead)
async def get_lesson(lesson_id: UUID, service: LessonService = Depends(LessonService)):
    return await service.get_lesson(lesson_id)


@lesson_router.post("", status_code=status.HTTP_201_CREATED, response_model=LessonRead)
async def create_lesson(info: LessonCreate, service: LessonService = Depends(LessonService)):
    return await service.create_lesson(info)


@lesson_router.delete("/{lesson_id}")
async def delete_lesson(lesson_id: UUID, service: LessonService = Depends(LessonService)):
    await service.delete_lesson(lesson_id)

@lesson_router.get("", response_model=List[LessonRead])
async def get_lessons(service: LessonService = Depends(LessonService)):
    return await service.get_lessons()

# Set quiz score for a specific lesson
@lesson_router.post("/quiz_score", status_code=status.HTTP_200_OK)
async def set_lesson_quiz_score(user_id: UUID, module_id: UUID, lesson_id: UUID, quiz_score: int, service: LessonService = Depends(LessonService)):
    return await service.set_lesson_quiz_score(user_id, module_id, lesson_id, quiz_score)

# Get quiz score for a user, module, and lesson
@lesson_router.get("/{module_id}/lesson/{lesson_id}/quiz_score/{user_id}", response_model=LessonRead)
async def get_lesson_quiz_score(module_id: UUID, lesson_id: UUID, user_id: UUID, service: LessonService = Depends(LessonService)):
    lesson = await service.get_lesson_quiz_score_for_user(module_id, lesson_id, user_id)
    return {
        "id": lesson.id,
        "name": lesson.name,
        "user_id": lesson.user_id,
        "module_id": lesson.module_id,
        "quiz_score": lesson.lesson_quiz
    }

# Increment lesson progress (lesson completed)
@lesson_router.post("/increment_progress", status_code=status.HTTP_200_OK)
async def increment_lesson_progress(user_id: UUID, module_id: UUID, lesson_id: UUID, lesson_completed: bool = False, service: LessonService = Depends(LessonService)):
    return await service.increment_lesson_progress(user_id, module_id, lesson_id, lesson_completed)

