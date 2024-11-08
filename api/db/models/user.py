from sqlmodel import Field, SQLModel, AutoString
from pydantic import EmailStr
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel


class UserBase(SQLModel):
    first_name: str = Field(None, description="First Name of the User")
    last_name: str = Field(None, description="Last Name of the User")
    email: EmailStr = Field(
        ..., description="Email address of the user", nullable=False, index=True, unique=True, sa_type=AutoString
    )
    phone_number: str = Field(None, description="Phone number of the user", unique=True, sa_type=AutoString)


class User(BaseModel, UserBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "users"

    def __repr__(self):
        return f"<User (id: {self.id}, email: {self.email})>"
