from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User

class MessageBase(SQLModel):
    sender_id: UUID = Field(..., foreign_key="users.id", description="ID of the sender user")
    receiver_id: UUID = Field(..., foreign_key="users.id", description="ID of the receiver user")
    message: str = Field(..., description="The content of the message", nullable=False)
    is_read: bool = Field(default=False)

class Message(BaseModel, MessageBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "messages"

    sender: "User" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Message.sender_id]"})
    receiver: "User" = Relationship(sa_relationship_kwargs={"foreign_keys": "[Message.receiver_id]"})

    def __repr__(self):
        return f"<Message (id: {self.id}, sender_id: {self.sender_id}, receiver_id: {self.receiver_id})>"