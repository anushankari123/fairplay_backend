from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import re

# Define the request body model
class MessageRequest(BaseModel):
    message: str

# Create an API Router
chat_router = APIRouter(prefix="/api/api1")

# Sanitize the incoming message (remove non-ASCII characters)
def sanitize_message(message: str) -> str:
    return re.sub(r'[^\x00-\x7F]+', '', message)

# Define the chatbot response endpoint
@chat_router.post("/")
async def chatbot_response(request: MessageRequest):
    external_url="https://web-production-38420.up.railway.app/api/api1/"
    sanitized_message = sanitize_message(request.message)  # Sanitize the incoming message
    data = {"message": sanitized_message}  # Prepare data to be sent to the external service

    # Send the sanitized message to the external service using httpx
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(external_url, json=data, headers={"Content-Type": "application/json"})
            response.raise_for_status()  # Check if response status is ok
            return {"response_text": response.json().get("response_text", "No response text")}
        except httpx.RequestError as e:
            return {"error": "RequestError", "message": str(e), "payload": data}
        except httpx.HTTPStatusError as e:
            return {"error": "HTTPStatusError", "status_code": e.response.status_code, "response_body": e.response.text, "payload": data}