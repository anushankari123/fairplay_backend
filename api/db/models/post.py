from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User

class PostBase(SQLModel):
    title: str = Field(..., description="Title of the post", nullable=False)
    description: str = Field(..., description="Description of the post", nullable=False)
    hashtag: str = Field(None, description="Hashtags associated with the post", nullable=True)
    image_url: str = Field(None, description="URL of the uploaded image", nullable=True)


class Post(BaseModel, PostBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "posts"

    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user who created the post")
    user: "User" = Relationship(back_populates="posts")

    def __repr__(self):
        return f"<Post (id: {self.id}, title: {self.title}, user_id: {self.user_id})>"