from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..services.gemini import GeminiService  # Adjusted to use the new GeminiService

gemini_router = APIRouter()

@gemini_router.get("/gemini", summary="Fetch Gemini model results")
async def get_gemini_response(prompt: str, max_tokens: int = Query(100, description="Maximum number of tokens for the response")):
    try:
        # Use the GeminiService to get the response
        response = await GeminiService.get_response(prompt=prompt)
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
