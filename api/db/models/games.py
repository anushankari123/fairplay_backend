from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User

class GameScoreBase(SQLModel):
    game_name: str = Field(..., description="Name of the game", nullable=False)
    score: int = Field(..., description="Score achieved in the game", nullable=False)
    cumulative_total: int = Field(..., description="Running total of all scores", nullable=False)

class GameScore(BaseModel, GameScoreBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "game_scores"

    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user who achieved the score")
    user: "User" = Relationship(back_populates="game_scores")

    def __repr__(self):
        return f"<GameScore (id: {self.id}, game: {self.game_name}, score: {self.score}, total: {self.cumulative_total})>"