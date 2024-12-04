from uuid import UUID
from sqlmodel import col
from api.db.models.post import Post
from api.interfaces.utils import List
from api.interfaces.post import PostRead, PostCreate, PostUpdate
from api.utils.exceptions import NotFoundError
from .base import BaseService


class PostService(BaseService):
    async def get_post(self, post_id: UUID) -> PostRead:
        """
        Retrieve a specific post by its UUID.

        Args:
        - post_id (UUID): The UUID of the post to retrieve.

        Returns:
        - PostRead: Details of the retrieved post.

        Raises:
        - NotFoundError: Raised if the post is not found.
        """
        res = await Post.get(db=self.db, filters=[Post.id == post_id, ~col(Post.is_deleted)])
        post = res.one_or_none()
        if post is None:
            raise NotFoundError("Post not found")
        return post

    async def get_posts(self) -> List[PostRead]:
        """
        Retrieve a list of non-deleted posts.

        Returns:
        - List[PostRead]: List of non-deleted posts.
        """
        res = await Post.get(db=self.db, filters=[~col(Post.is_deleted)])
        return {"data": res.all()}

    async def create_post(self, data: PostCreate) -> PostRead:
        """
        Create a new post.

        Args:
        - data (PostCreate): Information to create the post.

        Returns:
        - PostRead: Details of the created post.
        """
        new_post = Post(**data.model_dump())
        await new_post.save(self.db)
        return new_post

    async def delete_post(self, post_id: UUID):
        """
        Mark a post as deleted.

        Args:
        - post_id (UUID): The UUID of the post to delete.
        """
        post = await self.get_post(post_id)
        post.is_deleted = True
        await post.save(self.db)

    async def update_post(self, post_id: UUID, data: PostUpdate) -> PostRead:
        """
        Update details of a post.

        Args:
        - post_id (UUID): The UUID of the post to update.
        - data (PostUpdate): Information to update the post.

        Returns:
        - PostRead: Details of the updated post.
        """
        post = await self.get_post(post_id)
        await post.update(self.db, data)
        return post
    
    async def increment_like_count(self, post_id: UUID) -> PostRead:
        """
        Increment the like count of a post.
        """
        post = await self.get_post(post_id)
        post.like_count = post.like_count + 1 if post.like_count else 1
        await post.save(self.db)
        return post
    
    async def decrement_like_count(self, post_id: UUID) -> PostRead:
        """
        Decrement the like count of a post.
        """
        post = await self.get_post(post_id)
        if post.like_count and post.like_count > 0:
            post.like_count -= 1
        await post.save(self.db)
        return post
    
    async def get_posts_by_user(self, user_id: UUID) -> List[PostRead]:
        """
        Retrieve a list of posts created by a specific user.

        Args:
        - user_id (UUID): The UUID of the user whose posts are to be retrieved.

        Returns:
        - List[PostRead]: List of posts created by the user.
        """
        res = await Post.get(
            db=self.db,
            filters=[Post.user_id == user_id, ~col(Post.is_deleted)]
        )
        return {"data": res.all()}

