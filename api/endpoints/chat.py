from fastapi import APIRouter
from pydantic import BaseModel
import httpx

# Define the data model for the request body
class MessageRequest(BaseModel):
    message: str

# Initialize the router with the prefix directly
chat_router = APIRouter(prefix="/api/api1")

# Define the POST endpoint
@chat_router.post("/")
async def chatbot_response(request: MessageRequest):
    # URL of the external chatbot endpoint
    external_url = "https://web-production-dab9b.up.railway.app/api/api1/"

    # Prepare the data to be sent in the request
    data = {"message": request.message}

    # Make a request to the external chatbot service
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(external_url, json=data, headers={"Content-Type": "application/json"})
            response.raise_for_status()  # Raise an exception for any non-2xx status codes

            # Return the response from the external chatbot API
            return {"response_text": response.json().get("response_text", "No response text")}
        except httpx.RequestError as e:
            return {"error": f"An error occurred while requesting the chatbot: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error occurred: {e.response.status_code}"}

