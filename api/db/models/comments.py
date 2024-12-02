from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User
    from .post import Post

class CommentBase(SQLModel):
    like_count: int = Field(default=0, description="Number of likes on the comment")
    comment: str = Field(..., description="Text of the comment", nullable=False)
    


class Comment(BaseModel, CommentBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "comments"

    post_id: UUID = Field(..., foreign_key="posts.id", description="ID of the associated post")
    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user who created the comment")
    user: "User" = Relationship(back_populates="comments")
    post: "Post" = Relationship(back_populates="comments")

    def __repr__(self):
        return f"<Comment (id: {self.id}, post_id: {self.post_id}, user_id: {self.user_id})>"
