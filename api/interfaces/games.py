from typing import Optional
from uuid import UUID
from pydantic import ConfigDict
from sqlmodel import SQLModel
from api.db.models.games import GameScoreBase
from api.db.models import IdMixin, TimestampMixin

class GameScoreCreate(SQLModel):
    game_name: str
    score: int
    user_id: UUID
    model_config = ConfigDict(extra="forbid")

class GameScoreRead(GameScoreBase, IdMixin, TimestampMixin):
    user_id: UUID

class LeaderboardEntry(SQLModel):
    first_name: str
    total_score: int
    games_played: int

