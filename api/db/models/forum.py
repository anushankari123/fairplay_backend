from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, SQLModel, Relationship, AutoString
from uuid import UUID
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User

class ForumBase(SQLModel):
    forum_name: str = Field(..., description="Name of the forum", max_length=100, nullable=False)
    description: Optional[str] = Field(None, description="Forum description")
    image_url: Optional[str] = Field(None, description="URL of forum image", sa_type=AutoString)

class Forum(BaseModel, ForumBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "forums"

    # Use string-based relationship references
    forum_members: List["ForumMember"] = Relationship(back_populates="forum", sa_relationship_kwargs={"cascade": "all, delete"})
    forum_messages: List["ForumMessage"] = Relationship(back_populates="forum", sa_relationship_kwargs={"cascade": "all, delete"})

    def __repr__(self):
        return f"<Forum (id: {self.id}, name: {self.forum_name})>"

class ForumMemberBase(SQLModel):
    forum_id: UUID = Field(..., foreign_key="forums.id", description="ID of the forum")
    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user")

class ForumMember(BaseModel, ForumMemberBase, IdMixin, table=True):
    __tablename__ = "forum_members"

    # Use string-based relationship references
    forum: "Forum" = Relationship(back_populates="forum_members")
    user: "User" = Relationship(back_populates="forum_members")

    def __repr__(self):
        return f"<ForumMember (forum_id: {self.forum_id}, user_id: {self.user_id})>"

class ForumMessageBase(SQLModel):
    forum_id: UUID = Field(..., foreign_key="forums.id", description="ID of the forum")
    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the sender")
    message: str = Field(..., description="Message content", nullable=False)
    image_url: Optional[str] = Field(None, description="URL of the message image")

class ForumMessage(BaseModel, ForumMessageBase, IdMixin, TimestampMixin, table=True):
    __tablename__ = "forum_messages"

    # Use string-based relationship references
    forum: "Forum" = Relationship(back_populates="forum_messages")
    user: "User" = Relationship(back_populates="forum_messages")

    def __repr__(self):
        return f"<ForumMessage (id: {self.id}, forum_id: {self.forum_id}, user_id: {self.user_id})>"