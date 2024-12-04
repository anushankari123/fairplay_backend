# endpoints/messages.py
from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import MessageService
from api.interfaces.utils import List
from api.interfaces.messages import MessageRead, MessageCreate
from sqlalchemy import select
from api.db.models.messages import Message  # Import the Message model

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

@messages_router.get("/unread", response_model=dict)
async def get_unread_messages(
    user1_id: UUID, 
    user2_id: UUID, 
    service: MessageService = Depends(MessageService)
):
    """
    Get unread message count for a specific conversation.
    """
    query = select(Message).where(
        (Message.sender_id == user2_id) & 
        (Message.receiver_id == user1_id) & 
        (Message.is_read == False)
    )
    result = await service.db.execute(query)
    unread_count = len(result.scalars().all())
    
    return {"unreadCount": unread_count}
@messages_router.post("/mark-read", status_code=status.HTTP_200_OK)
async def mark_messages_read(
    user1_id: UUID,  
    user2_id: UUID,  
    service: MessageService = Depends(MessageService)
): 
    """ 
    Mark all unread messages in a conversation as read and update conversation last_read. 
    """ 
    # Mark messages as read
    await service.mark_messages_as_read(user1_id, user2_id)
    
    # Update the conversation's last_read timestamp
    await service.update_conversation_last_read(user1_id, user2_id)
    
    return {"message": "Messages marked as read"}