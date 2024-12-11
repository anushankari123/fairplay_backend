from typing import Optional
from pydantic import ConfigDict, EmailStr, field_validator
from sqlmodel import SQLModel
from uuid import UUID
from api.db.models.user import UserBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin
import re


class UserCreate(UserBase):
    model_config = ConfigDict(extra="forbid")



class UserRead(UserBase, IdMixin, TimestampMixin):
    id: UUID
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None  # Allow phone_number to be None
    password: Optional[str] = None
    age: Optional[int] = None
    bio: Optional[str] =None
    country: Optional[str] = None
    state: Optional[str] = None
    dp_url: Optional[str] =None


class UserReadInternal(UserRead, SoftDeleteMixin):
    pass


class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    age: Optional[int] = None
    bio: Optional[str] =None
    country: Optional[str] = None
    state: Optional[str] = None
    dp_url: Optional[str] =None

    model_config = ConfigDict(extra="forbid")


class UserLogin(SQLModel):
    email: EmailStr
    password: str
    category: str

    