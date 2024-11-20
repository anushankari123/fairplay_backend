from typing import Optional
from pydantic import ConfigDict, EmailStr, field_validator
from sqlmodel import SQLModel
from api.db.models.user import UserBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin
import re


class UserCreate(UserBase):
    model_config = ConfigDict(extra="forbid")

    @field_validator('password')
    @classmethod
    def validate_password(cls, password):
        # Password complexity validation
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one number')
        return password


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


class UserLogin(SQLModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(extra="forbid")