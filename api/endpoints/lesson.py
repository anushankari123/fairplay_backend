from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import LessonQuizService
from api.interfaces.utils import List
from api.interfaces.lesson import LessonQuizCreate, LessonQuizRead
from sqlmodel import SQLModel

class ScoreUpdate(SQLModel):
    score: int

lesson_router = APIRouter(prefix="/lesson-quizzes")

@lesson_router.get("/user/{user_id}")
async def get_lesson_quizzes_by_user(user_id: UUID, service: LessonQuizService = Depends(LessonQuizService)):
    """
    Retrieve lesson quizzes for a specific user.
    """
    return await service.get_lesson_quizzes_by_user(user_id)

@lesson_router.get("/{lesson_quiz_id}")
async def get_lesson_quiz_by_id(lesson_quiz_id: UUID, service: LessonQuizService = Depends(LessonQuizService)):
    """
    Retrieve a specific lesson quiz by its ID.
    """
    return await service.get_lesson_quiz_by_id(lesson_quiz_id)

@lesson_router.patch("/{lesson_quiz_id}/score")
async def update_lesson_quiz_score(
    lesson_quiz_id: UUID, 
    data: ScoreUpdate, 
    service: LessonQuizService = Depends(LessonQuizService)
):
    """
    Update lesson quiz score conditionally.
    """
    return await service.update_lesson_quiz_score(lesson_quiz_id, data.score)

@lesson_router.post("", status_code=status.HTTP_201_CREATED, response_model=LessonQuizRead)
async def create_lesson_quiz(
    info: LessonQuizCreate,
    service: LessonQuizService = Depends(LessonQuizService),
):
    """
    Create a module quiz or fetch an existing one if the combination of
    user_id and module_name already exists.
    """
    return await service.create_lesson_quiz(info)

@lesson_router.delete("/{lesson_quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson_quiz(lesson_quiz_id: UUID, service: LessonQuizService = Depends(LessonQuizService)):
    """
    Endpoint to delete a module quiz.
    """
    await service.delete_lesson_quiz(lesson_quiz_id)