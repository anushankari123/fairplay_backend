from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, AutoString, Relationship
from pydantic import EmailStr
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .post import Post
    from .games import GameScore


class UserBase(SQLModel):
    first_name: str = Field(None, description="First Name of the User")
    last_name: str = Field(None, description="Last Name of the User")
    email: EmailStr = Field(
        ..., description="Email address of the user", nullable=False, index=True, unique=True, sa_type=AutoString
    )
    phone_number: str = Field(None, description="Phone number of the user", unique=False, sa_type=AutoString)
    password: str = Field(..., description="Hashed password of the user", nullable=False, sa_type=AutoString)


class User(BaseModel, UserBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "users"

    posts: list["Post"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    game_scores: list["GameScore"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    def __repr__(self):
        return f"<User (id: {self.id}, email: {self.email})>"