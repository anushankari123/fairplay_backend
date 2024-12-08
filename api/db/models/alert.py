from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User

class AlertBase(SQLModel):
    name: str = Field(..., description="Name of the alert", nullable=False)
    description: str = Field(..., description="Description of the alert", nullable=False)
    alert_datetime: datetime = Field(..., description="Date and time when the alert should trigger", nullable=False)

class Alert(BaseModel, AlertBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "alerts"

    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user who created the alert")
    user: "User" = Relationship(back_populates="alerts")
    
    def __repr__(self):
        return f"<Alert (id: {self.id}, name: {self.name}, user_id: {self.user_id}, alert_datetime: {self.alert_datetime})>"
