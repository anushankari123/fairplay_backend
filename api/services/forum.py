from uuid import UUID
from sqlmodel import select, col
from api.db.models.forum import Forum, ForumMember, ForumMessage
from api.db.models.user import User
from sqlalchemy.orm import joinedload
from api.interfaces.utils import List
from api.interfaces.forum import (
    ForumCreate, 
    ForumRead, 
    ForumMemberCreate, 
    ForumMemberRead, 
    ForumMessageCreate, 
    ForumMessageRead
)
from api.utils.exceptions import NotFoundError, ConflictError
from api.utils.spam_filter import SpamFilter
from .base import BaseService

class ForumService(BaseService):
    async def create_forum(self, data: ForumCreate) -> ForumRead:
        """
        Create a new forum.
        """
        new_forum = Forum(**data.model_dump())
        await new_forum.save(self.db)
        return new_forum

    async def add_forum_member(self, data: ForumMemberCreate) -> ForumMemberRead:
        """
        Add a user to a forum.
        """
        # Check if forum exists
        forum_query = select(Forum).where(Forum.id == data.forum_id, ~col(Forum.is_deleted))
        forum = await self.db.scalar(forum_query)
        if not forum:
            raise NotFoundError("Forum not found")

        # Check if user exists
        user_query = select(User).where(User.id == data.user_id, ~col(User.is_deleted))
        user = await self.db.scalar(user_query)
        if not user:
            raise NotFoundError("User not found")

        # Check if user is already a member
        existing_member_query = select(ForumMember).where(
            ForumMember.forum_id == data.forum_id, 
            ForumMember.user_id == data.user_id
        )
        existing_member = await self.db.scalar(existing_member_query)
        if existing_member:
            raise ConflictError("User is already a member of this forum")

        # Create forum member
        new_member = ForumMember(**data.model_dump())
        await new_member.save(self.db)
        return new_member

    async def send_forum_message(self, data: ForumMessageCreate) -> ForumMessageRead:
        """
        Send a message to a forum.
        """
        # Check if forum exists
        forum_query = select(Forum).where(Forum.id == data.forum_id, ~col(Forum.is_deleted))
        forum = await self.db.scalar(forum_query)
        if not forum:
            raise NotFoundError("Forum not found")

        # Check for promotional content
        # Check for promotional content
        if SpamFilter.detect_promotional_content(data.message):
            raise ConflictError("Message content detected as promotional and rejected.")

        # Create forum message
        new_message = ForumMessage(**data.model_dump())
        await new_message.save(self.db)
        
        # Add user name to response
        user_query = select(User).where(User.id == data.user_id)
        user = await self.db.scalar(user_query)
        
        # Create response using model_dump to include all fields
        message_dict = new_message.model_dump()
        message_dict['user_name'] = f"{user.first_name} {user.last_name}" if user else None
        
        return ForumMessageRead(**message_dict)

    async def get_forum_members(self, forum_id: UUID) -> List[ForumMemberRead]:
        """
        Get all members of a specific forum.
        """
        query = (
            select(ForumMember)
            .join(User)
            .where(ForumMember.forum_id == forum_id)
        )
        result = await self.db.execute(query)
        return {"data": result.scalars().all()}

    async def get_forum_messages(self, forum_id: UUID) -> List[ForumMessageRead]:
        """
        Get all messages in a specific forum.
        """
        query = (
            select(ForumMessage)
            .options(
                joinedload(ForumMessage.user)
            )
            .where(
                ForumMessage.forum_id == forum_id
            )
            .order_by(ForumMessage.created_at)
        )
        result = await self.db.execute(query)
        messages = result.scalars().all()

        # Format the response to include user names
        response = [
            ForumMessageRead(
                **message.model_dump(), 
                user_name=f"{message.user.first_name} {message.user.last_name}" if message.user else None
            )
            for message in messages
        ]

        return {"data": response}

    async def list_forums(self) -> List[ForumRead]:
        """
        List all forums.
        """
        query = select(Forum).where(~col(Forum.is_deleted))
        result = await self.db.execute(query)
        return {"data": result.scalars().all()}
    
    async def delete_forum(self, forum_id: UUID) -> None:
        """
        Mark a forum as deleted.
        
        Args:
        - forum_id (UUID): The UUID of the forum to delete.
        """
        # Fetch the forum to be deleted
        forum_query = select(Forum).where(Forum.id == forum_id, ~col(Forum.is_deleted))
        forum = await self.db.scalar(forum_query)
        
        if not forum:
            raise NotFoundError("Forum not found or already deleted")

        # Mark the forum as deleted
        forum.is_deleted = True
        await forum.save(self.db)