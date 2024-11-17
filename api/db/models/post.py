from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User


class PostBase(SQLModel):
    description: str = Field(..., description="Description of the post", nullable=False)
    hashtag: str = Field(..., description="Hashtags associated with the post", nullable=True)
    photo: str = Field(..., description="URL or path to the photo associated with the post", nullable=True)


class Post(BaseModel, PostBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "posts"

    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user who created the post")
    user: "User" = Relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post (id: {self.id}, description: {self.description}, user_id: {self.user_id})>"
