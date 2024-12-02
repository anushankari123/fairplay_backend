from uuid import UUID
from sqlmodel import col
from api.db.models.comments import Comment
from api.interfaces.comments import CommentRead, CommentCreate, CommentUpdate
from api.interfaces.utils import List
from api.utils.exceptions import NotFoundError
from .base import BaseService


class CommentService(BaseService):
    async def get_comment(self, comment_id: UUID) -> CommentRead:
        """
        Retrieve a specific comment by its UUID.
        """
        res = await Comment.get(db=self.db, filters=[Comment.id == comment_id, ~col(Comment.is_deleted)])
        comment = res.one_or_none()
        if comment is None:
            raise NotFoundError("Comment not found")
        return comment

    async def get_comments_for_post(self, post_id: UUID) -> List[CommentRead]:
        """
        Retrieve all comments for a specific post.
        """
        res = await Comment.get(db=self.db, filters=[Comment.post_id == post_id, ~col(Comment.is_deleted)])
        return {"data": res.all()}

    async def create_comment(self, data: CommentCreate) -> CommentRead:
        """
        Create a new comment.
        """
        new_comment = Comment(**data.model_dump())
        await new_comment.save(self.db)
        return new_comment

    async def delete_comment(self, comment_id: UUID):
        """
        Mark a comment as deleted.
        """
        comment = await self.get_comment(comment_id)
        comment.is_deleted = True
        await comment.save(self.db)

    async def update_comment(self, comment_id: UUID, data: CommentUpdate) -> CommentRead:
        """
        Update details of a comment.
        """
        comment = await self.get_comment(comment_id)
        await comment.update(self.db, data)
        return comment

    async def increment_like_count(self, comment_id: UUID) -> CommentRead:
        """
        Increment the like count of a comment.
        """
        comment = await self.get_comment(comment_id)
        comment.like_count += 1
        await comment.save(self.db)
        return comment
    
    
