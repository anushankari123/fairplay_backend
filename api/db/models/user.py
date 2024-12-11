from typing import TYPE_CHECKING, Optional
from enum import Enum
from sqlmodel import Field, SQLModel, AutoString, Relationship
from pydantic import EmailStr
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .post import Post
    from .games import GameScore
    from .comments import Comment
    from .forum import ForumMember, ForumMessage
    from .module import ModuleQuiz
    from .lesson import LessonQuiz
    from .alert import Alert
    from .certificate import Certificate


class UserCategory(str, Enum):
    COACH = "coach"
    ATHELETE = "atheletes"
    OTHERS= "others"
    STUDENT = "student"
    EXPERTS= "experts"


class UserBase(SQLModel):
    first_name: str = Field(None, description="First Name of the User")
    last_name: str = Field(None, description="Last Name of the User")
    email: EmailStr = Field(
        ..., description="Email address of the user", nullable=False, index=True, unique=True, sa_type=AutoString
    )
    phone_number: str = Field(None, description="Phone number of the user", unique=False, sa_type=AutoString)
    password: str = Field(..., description="Hashed password of the user", nullable=False, sa_type=AutoString)
    age: Optional[int] = Field(None, description="Age of the user")
    bio: Optional[str] = Field(None, description="Bio of the user")
    country: Optional[str] = Field(None, description="Country of the user")
    state: Optional[str] = Field(None, description="State of the user")
    dp_url: Optional[str] = Field(None, description="URL of the uploaded image")
    category: UserCategory = Field(
        ..., description="Category of the user (e.g., coach, player, professional, student)"
    )


class User(BaseModel, UserBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "users"

    posts: list["Post"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    game_scores: list["GameScore"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    comments: list["Comment"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    forum_members: list["ForumMember"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    forum_messages: list["ForumMessage"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    module_quizzes: list["ModuleQuiz"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    lesson_quizzes: list["LessonQuiz"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    alerts: list["Alert"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    certificates: list["Certificate"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    def __repr__(self):
        return f"<User (id: {self.id}, email: {self.email}, category: {self.category})>"
