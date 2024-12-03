from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.utils.exceptions import NotFoundError, HTTPException
from api.services import ForumService
from api.interfaces.utils import List
from api.interfaces.forum import (
    ForumCreate, 
    ForumRead, 
    ForumMemberCreate, 
    ForumMemberRead, 
    ForumMessageCreate, 
    ForumMessageRead
)

forum_router = APIRouter(prefix="/forums")

@forum_router.post("", status_code=status.HTTP_201_CREATED, response_model=ForumRead)
async def create_forum(info: ForumCreate, service: ForumService = Depends(ForumService)):
    """
    Create a new forum.
    """
    return await service.create_forum(info)

@forum_router.post("/members", status_code=status.HTTP_201_CREATED, response_model=ForumMemberRead)
async def add_forum_member(info: ForumMemberCreate, service: ForumService = Depends(ForumService)):
    """
    Add a user to a forum.
    """
    return await service.add_forum_member(info)

@forum_router.post("/messages", status_code=status.HTTP_201_CREATED, response_model=ForumMessageRead)
async def send_forum_message(info: ForumMessageCreate, service: ForumService = Depends(ForumService)):
    """
    Send a message to a forum.
    """
    return await service.send_forum_message(info)

@forum_router.get("/{forum_id}/members", response_model=List[ForumMemberRead])
async def get_forum_members(forum_id: UUID, service: ForumService = Depends(ForumService)):
    """
    Get all members of a specific forum.
    """
    return await service.get_forum_members(forum_id)

@forum_router.get("/{forum_id}/messages", response_model=List[ForumMessageRead])
async def get_forum_messages(forum_id: UUID, service: ForumService = Depends(ForumService)):
    """
    Get all messages in a specific forum.
    """
    return await service.get_forum_messages(forum_id)

@forum_router.get("", response_model=List[ForumRead])
async def list_forums(service: ForumService = Depends(ForumService)):
    """
    List all forums.
    """
    return await service.list_forums()

@forum_router.delete("/{forum_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_forum(forum_id: UUID, service: ForumService = Depends(ForumService)):
    """
    Mark a forum as deleted.
    
    Args:
    - forum_id (UUID): The UUID of the forum to delete.
    """
    try:
        await service.delete_forum(forum_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Forum not found")
