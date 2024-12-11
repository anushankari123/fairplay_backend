from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from api.db.models.alert import AlertBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin
class AlertCreate(BaseModel):
    name: str
    description: str
    alert_datetime: datetime
class AlertRead(AlertCreate):
    id: UUID
    user_id: UUID
    class Config:
        orm_mode = True