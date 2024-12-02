# endpoints/messages.py
from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import MessageService
from api.interfaces.utils import List
from api.interfaces.messages import MessageRead, MessageCreate

messages_router = APIRouter(prefix="/messages")

@messages_router.post("", status_code=status.HTTP_201_CREATED, response_model=MessageRead)
async def send_message(info: MessageCreate, service: MessageService = Depends(MessageService)):
    """
    Send a new message.
    """
    return await service.send_message(info)

@messages_router.get("/user/{user_id}", response_model=List[MessageRead])
async def get_user_messages(user_id: UUID, service: MessageService = Depends(MessageService)):
    """
    Get all messages sent to or received by a user.
    """
    return await service.get_user_messages(user_id)

@messages_router.get("/conversation", response_model=List[MessageRead])
async def get_conversation(user1_id: UUID, user2_id: UUID, service: MessageService = Depends(MessageService)):
    """
    Get all messages exchanged between two users.
    """
    return await service.get_conversation(user1_id, user2_id)
