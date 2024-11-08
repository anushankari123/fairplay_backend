from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import UserService
from api.interfaces.utils import List
from api.interfaces.user import UserRead, UserCreate, UserUpdate

user_router = APIRouter(prefix="/users")


@user_router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, service: UserService = Depends(UserService)):
    """
    Endpoint to get a user details
    """
    return await service.get_user(user_id)


@user_router.get("", response_model=List[UserRead])
async def get_users(service: UserService = Depends(UserService)):
    """
    Endpoint to get a list of user
    """
    return await service.get_users()


@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(info: UserCreate, service: UserService = Depends(UserService)):
    """
    Endpoint to create a user
    """
    return await service.create_user(info)


@user_router.delete("/{user_id}")
async def delete_user(user_id: UUID, service: UserService = Depends(UserService)):
    """
    Endpoint to delete a user
    """
    await service.delete_user(user_id)


@user_router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: UUID, info: UserUpdate, service: UserService = Depends(UserService)):
    """
    Endpoint to update the given user details
    """
    return await service.update_user(user_id, info)
