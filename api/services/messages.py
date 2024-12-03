from uuid import UUID
from sqlmodel import select, col
from api.db.models.messages import Message
from sqlalchemy.orm import joinedload
from api.db.models.user import User
from api.interfaces.utils import List
from api.interfaces.messages import MessageRead, MessageCreate
from api.utils.exceptions import NotFoundError
from .base import BaseService

class MessageService(BaseService):
    async def send_message(self, data: MessageCreate) -> MessageRead:
        """
        Create and save a new message.
        """
        new_message = Message(**data.model_dump())
        await new_message.save(self.db)
        return new_message

    async def get_user_messages(self, user_id: UUID) -> List[MessageRead]:
        """
        Get all messages sent to or from a specific user.
        """
        query = select(Message).where(
            (Message.sender_id == user_id) | (Message.receiver_id == user_id),
            ~col(Message.is_deleted)
        )
        result = await self.db.execute(query)
        return {"data": result.scalars().all()}

    async def get_conversation(self, user1_id: UUID, user2_id: UUID) -> List[dict]:
        """
        Get all messages exchanged between two users along with sender and receiver names.
        """
        query = (
            select(Message)
            .options(
                joinedload(Message.sender),  # Load sender relationship
                joinedload(Message.receiver)  # Load receiver relationship
            )
            .where(
                (
                    (Message.sender_id == user1_id) & (Message.receiver_id == user2_id)
                ) | (
                    (Message.sender_id == user2_id) & (Message.receiver_id == user1_id)
                ),
                ~col(Message.is_deleted)
            )
            .order_by(Message.created_at)
        )
        result = await self.db.execute(query)
        messages = result.scalars().all()

        # Format the response to include sender and receiver names
        response = [
            {
                "id": message.id,
                "message": message.message,
                "created_at": message.created_at,
                "sender_id": message.sender_id,
                "receiver_id": message.receiver_id,
                "sender_name": f"{message.sender.first_name} {message.sender.last_name}" if message.sender else None,
                "receiver_name": f"{message.receiver.first_name} {message.receiver.last_name}" if message.receiver else None,
            }
            for message in messages
        ]

        return {"data": response}
