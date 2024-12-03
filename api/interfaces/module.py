from typing import Optional
from uuid import UUID
from pydantic import ConfigDict
from sqlmodel import SQLModel
from api.db.models.module import ModuleBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin


class ModuleCreate(SQLModel):
    user_id: UUID
    name: str
    image_url: Optional[str] = None
    model_config = ConfigDict(extra="forbid")


class ModuleRead(ModuleBase, IdMixin, TimestampMixin):
    user_id: UUID



class ModuleUpdate(SQLModel):
    quiz_score: Optional[int] = None
    modules_completed: Optional[int] = None
    modules_in_progress: Optional[int] = None
    model_config = ConfigDict(extra="forbid")
