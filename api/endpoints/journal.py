from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..services.journal import JournalService

journal_router = APIRouter()

@journal_router.get("/journals", summary="Get scientific journals related to doping")
async def get_doping_journals(page: int = Query(1, description="Page number for pagination")):
    """
    Endpoint to fetch scientific journals related to doping
    
    :param page: Page number for pagination
    :return: Dictionary with journal data and pagination info
    """
    try:
        journals = JournalService.fetch_journals(page=page)
        return {
            "status": "success", 
            "data": journals, 
            "hasMore": len(journals) == 20
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))