from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..services.news import NewsService

news_router = APIRouter()

@news_router.get("/news", summary="Get English news related to doping and anti-doping")
async def get_anti_doping_news(page: int = Query(1, description="Page number for pagination")):
    try:
        news = NewsService.fetch_news(page=page)
        return {"status": "success", "data": news, "hasMore": len(news) == 20}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))