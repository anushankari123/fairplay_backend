from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import GameScoreService
from api.interfaces.utils import List
from api.interfaces.games import GameScoreRead, GameScoreCreate, LeaderboardEntry

games_router = APIRouter(prefix="/game-scores")

@games_router.post("", status_code=status.HTTP_201_CREATED, response_model=GameScoreRead)
async def record_score(info: GameScoreCreate, service: GameScoreService = Depends(GameScoreService)):
    """
    Record a new game score
    """
    return await service.record_score(info)

@games_router.get("/user/{user_id}", response_model=List[GameScoreRead])
async def get_user_scores(user_id: UUID, service: GameScoreService = Depends(GameScoreService)):
    """
    Get all scores for a specific user
    """
    return await service.get_user_scores(user_id)

@games_router.get("/game/{game_name}", response_model=List[GameScoreRead])
async def get_game_scores(game_name: str, service: GameScoreService = Depends(GameScoreService)):
    """
    Get all scores for a specific game
    """
    return await service.get_game_scores(game_name)

@games_router.get("/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(service: GameScoreService = Depends(GameScoreService)):
    """
    Get the global leaderboard
    """
    return await service.get_leaderboard()

@games_router.get("/user/{user_id}/total", response_model=dict)
async def get_user_total(user_id: UUID, service: GameScoreService = Depends(GameScoreService)):
    """
    Get user's total score across all games
    """
    return await service.get_user_total(user_id)