import os
from typing import Callable
from fastapi.requests import Request
from api.utils.exceptions import HTTPError
from api.db.session import get_session


async def http_exception_handler(request: Request, exc: HTTPError):
    # TODO: Log error for http exceptions
    # logger.error(
    #     "HTTPError",
    #     error=exc.error_name,
    #     status_code=exc.status_code,
    #     detail=exc.detail,
    #     route=str(permission),
    #     user=user
    # )
    if hasattr(request.state, "session"):
        await request.state.session.rollback()
        # TODO: Log rollback -- remove the rollback from api.db.models.base
        # logger.info("Automatically rollback session")
    if os.environ.get("RAISE_HTTP_EXCEPTION") == "true":
        # for testing purpose
        raise exc
    return exc.json_response


class HandlerMiddleware:
    """
    Middleware to handle the HTTP Errors
    """

    async def __call__(self, request: Request, call_next: Callable):
        try:
            request.state.session = await anext(get_session())
            resp = await call_next(request)
            await request.state.session.commit()
            return resp
        except HTTPError as err:
            return await http_exception_handler(request, err)
