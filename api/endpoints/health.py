from fastapi import APIRouter

from api.interfaces import PingResponse, HealthResponse

health_router = APIRouter(prefix="")
# health_router = APIRouter(prefix="", include_in_schema=False)


@health_router.get("/ping", response_model=PingResponse)
async def ping() -> PingResponse:
    """
    Endpoint to check if the API system is alive
    """
    return {"msg": "pong"}


@health_router.get("/health", response_model=HealthResponse)
async def health() -> PingResponse:
    """
    Endpoint to check if the health of API system
    This includes DB and other services that api interacts with
    """
    # add the health info for DB and other services later when they are added
    return {"api": "OK"}
