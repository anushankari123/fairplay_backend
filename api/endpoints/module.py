from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import ModuleService
from api.interfaces.utils import List
from api.interfaces.module import ModuleRead, ModuleCreate, ModuleUpdate

module_router = APIRouter(prefix="/modules")


@module_router.get("/{module_id}", response_model=ModuleRead)
async def get_module(module_id: UUID, service: ModuleService = Depends(ModuleService)):
    return await service.get_module(module_id)


@module_router.post("", status_code=status.HTTP_201_CREATED, response_model=ModuleRead)
async def create_module(info: ModuleCreate, service: ModuleService = Depends(ModuleService)):
    return await service.create_module(info)


@module_router.delete("/{module_id}")
async def delete_module(module_id: UUID, service: ModuleService = Depends(ModuleService)):
    await service.delete_module(module_id)

@module_router.get("", response_model=List[ModuleRead])
async def get_modules(service: ModuleService = Depends(ModuleService)):
    return await service.get_modules()

@module_router.post("/quiz_score", status_code=status.HTTP_200_OK)
async def set_quiz_score(user_id: UUID, module_id: UUID, quiz_score: int, service: ModuleService = Depends(ModuleService)):
    return await service.set_quiz_score(user_id, module_id, quiz_score)

# Get quiz score for a user and module
@module_router.get("/{module_id}/quiz_score/{user_id}", response_model=ModuleRead)
async def get_quiz_score(module_id: UUID, user_id: UUID, service: ModuleService = Depends(ModuleService)):
    module = await service.get_quiz_score_for_user(module_id, user_id)
    # Return the complete module object (including name and user_id)
    return {
        "id": module.id,
        "name": module.name,
        "user_id": module.user_id,
        "quiz_score": module.quiz_score
    }

# Increment module progress (completed or in progress)
@module_router.post("/increment_progress", status_code=status.HTTP_200_OK)
async def increment_progress(user_id: UUID, increment_completed: bool = False, increment_in_progress: bool = False, service: ModuleService = Depends(ModuleService)):
    return await service.increment_module_progress(user_id, increment_completed, increment_in_progress)



