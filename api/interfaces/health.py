from pydantic import BaseModel, Field


class PingResponse(BaseModel):
    """
    A simple Model for Response of Ping endpoint
    """

    msg: str = Field(..., description="A message that will be echoed back by the API system")


class HealthResponse(BaseModel):
    """
    A simple Model for Response of Health endpoint
    """

    api: str = Field(..., description="A message on health of the api system")
