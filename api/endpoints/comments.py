from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import CommentService
from api.interfaces.comments import CommentRead, CommentCreate, CommentUpdate
from api.interfaces.utils import List

comments_router = APIRouter(prefix="/comments")


@comments_router.get("/{comment_id}", response_model=CommentRead)
async def get_comment(comment_id: UUID, service: CommentService = Depends(CommentService)):
    """
    Endpoint to get a specific comment
    """
    return await service.get_comment(comment_id)


@comments_router.get("/post/{post_id}", response_model=List[CommentRead])
async def get_comments_for_post(post_id: UUID, service: CommentService = Depends(CommentService)):
    """
    Endpoint to get all comments for a particular post
    """
    return await service.get_comments_for_post(post_id)


@comments_router.post("", status_code=status.HTTP_201_CREATED, response_model=CommentRead)
async def create_comment(info: CommentCreate, service: CommentService = Depends(CommentService)):
    """
    Endpoint to create a comment
    """
    return await service.create_comment(info)


@comments_router.delete("/{comment_id}")
async def delete_comment(comment_id: UUID, service: CommentService = Depends(CommentService)):
    """
    Endpoint to delete a comment
    """
    await service.delete_comment(comment_id)


@comments_router.patch("/{comment_id}", response_model=CommentRead)
async def update_comment(comment_id: UUID, info: CommentUpdate, service: CommentService = Depends(CommentService)):
    """
    Endpoint to update the given comment
    """
    return await service.update_comment(comment_id, info)


@comments_router.post("/{comment_id}/like", response_model=CommentRead)
async def increment_like_count(comment_id: UUID, service: CommentService = Depends(CommentService)):
    """
    Endpoint to increment the like count for a comment
    """
    return await service.increment_like_count(comment_id)
