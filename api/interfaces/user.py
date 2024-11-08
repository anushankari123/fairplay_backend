from typing import Optional
from pydantic import ConfigDict, EmailStr
from sqlmodel import SQLModel
from api.db.models.user import UserBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin


class UserCreate(UserBase):
    model_config = ConfigDict(extra="forbid")


class UserRead(UserBase, IdMixin, TimestampMixin):
    pass


class UserReadInternal(UserRead, SoftDeleteMixin):
    pass


class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    model_config = ConfigDict(extra="forbid")
