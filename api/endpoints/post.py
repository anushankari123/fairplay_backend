from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import PostService
from api.interfaces.utils import List
from api.interfaces.post import PostRead, PostCreate, PostUpdate

post_router = APIRouter(prefix="/posts")


@post_router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: UUID, service: PostService = Depends(PostService)):
    """
    Endpoint to get post details
    """
    return await service.get_post(post_id)


@post_router.get("", response_model=List[PostRead])
async def get_posts(service: PostService = Depends(PostService)):
    """
    Endpoint to get a list of posts
    """
    return await service.get_posts()


@post_router.post("", status_code=status.HTTP_201_CREATED, response_model=PostRead)
async def create_post(info: PostCreate, service: PostService = Depends(PostService)):
    """
    Endpoint to create a post
    """
    return await service.create_post(info)


@post_router.delete("/{post_id}")
async def delete_post(post_id: UUID, service: PostService = Depends(PostService)):
    """
    Endpoint to delete a post
    """
    await service.delete_post(post_id)


@post_router.patch("/{post_id}", response_model=PostRead)
async def update_post(post_id: UUID, info: PostUpdate, service: PostService = Depends(PostService)):
    """
    Endpoint to update the given post details
    """
    return await service.update_post(post_id, info)

@post_router.post("/{post_id}/like", response_model=PostRead, summary="Increment post like count")
async def like_post(post_id: UUID, post_service: PostService = Depends(PostService)):
    """
    Increment the like count of a post.
    """
    return await post_service.increment_like_count(post_id)


@post_router.post("/{post_id}/unlike", response_model=PostRead, summary="Decrement post like count")
async def unlike_post(post_id: UUID, post_service: PostService = Depends(PostService)):
    """
    Decrement the like count of a post.
    """
    return await post_service.decrement_like_count(post_id)

@post_router.get("/user/{user_id}", response_model=List[PostRead])
async def get_posts_by_user(user_id: UUID, service: PostService = Depends(PostService)):
    """
    Endpoint to get posts created by a specific user.
    """
    return await service.get_posts_by_user(user_id)
