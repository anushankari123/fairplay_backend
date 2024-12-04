from typing import Optional
from uuid import UUID
from pydantic import ConfigDict
from sqlmodel import SQLModel
from api.db.models.module import ModuleQuizBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin

class ModuleQuizCreate(ModuleQuizBase):
    user_id: UUID
    model_config = ConfigDict(extra="forbid")

class ModuleQuizRead(ModuleQuizBase, IdMixin, TimestampMixin):
    user_id: UUID

class ModuleQuizUpdate(SQLModel):
    module_name: Optional[str] = None
    module_progress: Optional[int] = None
    module_completed: Optional[int] = None
    m_quizscore: Optional[int] = None

    model_config = ConfigDict(extra="forbid")