# interfaces/messages.py
from uuid import UUID
from pydantic import ConfigDict
from sqlmodel import SQLModel
from api.db.models.messages import MessageBase
from api.db.models import IdMixin, TimestampMixin

class MessageCreate(SQLModel):
    sender_id: UUID
    receiver_id: UUID
    message: str
    model_config = ConfigDict(extra="forbid")

class MessageRead(MessageBase, IdMixin, TimestampMixin):
    pass
