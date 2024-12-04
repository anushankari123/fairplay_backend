from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import ModuleQuizService
from api.interfaces.utils import List
from api.interfaces.module import ModuleQuizCreate, ModuleQuizRead
from sqlmodel import SQLModel

class ScoreUpdate(SQLModel):
    score: int

module_router = APIRouter(prefix="/module-quizzes")

@module_router.get("/user/{user_id}")
async def get_module_quizzes_by_user(user_id: UUID, service: ModuleQuizService = Depends(ModuleQuizService)):
    """
    Retrieve module quizzes for a specific user.
    """
    return await service.get_module_quizzes_by_user(user_id)

@module_router.get("/{module_quiz_id}")
async def get_module_quiz_by_id(module_quiz_id: UUID, service: ModuleQuizService = Depends(ModuleQuizService)):
    """
    Retrieve a specific module quiz by its ID.
    """
    return await service.get_module_quiz_by_id(module_quiz_id)

@module_router.patch("/{module_quiz_id}/progress")
async def increment_module_progress(module_quiz_id: UUID, service: ModuleQuizService = Depends(ModuleQuizService)):
    """
    Increment module progress.
    """
    return await service.increment_module_progress(module_quiz_id)

@module_router.patch("/{module_quiz_id}/completed")
async def increment_module_completed(module_quiz_id: UUID, service: ModuleQuizService = Depends(ModuleQuizService)):
    """
    Increment module completed status.
    """
    return await service.increment_module_completed(module_quiz_id)

@module_router.patch("/{module_quiz_id}/score")
async def update_module_quiz_score(
    module_quiz_id: UUID, 
    data: ScoreUpdate, 
    service: ModuleQuizService = Depends(ModuleQuizService)
):
    """
    Update module quiz score conditionally.
    """
    return await service.update_module_quiz_score(module_quiz_id, data.score)

@module_router.post("", status_code=status.HTTP_201_CREATED, response_model=ModuleQuizRead)
async def create_module_quiz(
    info: ModuleQuizCreate,
    service: ModuleQuizService = Depends(ModuleQuizService),
):
    """
    Create a module quiz or fetch an existing one if the combination of
    user_id and module_name already exists.
    """
    return await service.create_module_quiz(info)

@module_router.delete("/{module_quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module_quiz(module_quiz_id: UUID, service: ModuleQuizService = Depends(ModuleQuizService)):
    """
    Endpoint to delete a module quiz.
    """
    await service.delete_module_quiz(module_quiz_id)

@module_router.get("/users/{user_id}/module-progress", response_model=dict)
async def get_total_progress_and_completed(
    user_id: UUID,
    module_quiz_service: ModuleQuizService = Depends(ModuleQuizService)
):
    """
    Get the total progress and completed module quizzes for a specific user.

    Args:
    - user_id (UUID): The ID of the user.

    Returns:
    - dict: A dictionary containing total progress and total completed.
    """
    try:
        result = await module_quiz_service.get_total_progress_and_completed(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))