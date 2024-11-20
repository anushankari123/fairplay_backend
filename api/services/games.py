from uuid import UUID
from sqlmodel import col, select, func
from api.db.models.games import GameScore
from api.db.models.user import User
from api.interfaces.utils import List
from api.interfaces.games import GameScoreRead, GameScoreCreate, LeaderboardEntry
from api.utils.exceptions import NotFoundError
from .base import BaseService

class GameScoreService(BaseService):
    async def record_score(self, data: GameScoreCreate) -> GameScoreRead:
        """
        Record a new game score and update cumulative total.

        Args:
        - data (GameScoreCreate): Score information to record

        Returns:
        - GameScoreRead: Details of the recorded score
        """
        # Get the user's current total score
        query = select(func.coalesce(func.max(GameScore.cumulative_total), 0)).where(
            GameScore.user_id == data.user_id,
            ~col(GameScore.is_deleted)
        )
        result = await self.db.execute(query)
        current_total = result.scalar() or 0
        
        # Create new score record with updated cumulative total
        new_score = GameScore(
            **data.model_dump(),
            cumulative_total=current_total + data.score
        )
        await new_score.save(self.db)
        return new_score

    async def get_user_scores(self, user_id: UUID) -> List[GameScoreRead]:
        """
        Get all scores for a specific user.

        Args:
        - user_id (UUID): The user's UUID

        Returns:
        - List[GameScoreRead]: List of user's scores
        """
        res = await GameScore.get(
            db=self.db,
            filters=[
                GameScore.user_id == user_id,
                ~col(GameScore.is_deleted)
            ]
        )
        return {"data": res.all()}

    async def get_game_scores(self, game_name: str) -> List[GameScoreRead]:
        """
        Get all scores for a specific game.

        Args:
        - game_name (str): Name of the game

        Returns:
        - List[GameScoreRead]: List of scores for the game
        """
        res = await GameScore.get(
            db=self.db,
            filters=[
                GameScore.game_name == game_name,
                ~col(GameScore.is_deleted)
            ]
        )
        return {"data": res.all()}

    async def get_leaderboard(self) -> List[LeaderboardEntry]:
            """
            Get global leaderboard across all games, including user's first name.

            Returns:
            - List[LeaderboardEntry]: Global leaderboard sorted by total score
            """
            query = select(
                User.first_name,
                func.sum(GameScore.score).label("total_score"),
                func.count(GameScore.id).label("games_played")
            ).join(
                User, GameScore.user_id == User.id
            ).where(
                ~col(GameScore.is_deleted)
            ).group_by(
                User.first_name
            ).order_by(
                func.sum(GameScore.score).desc()
            )
            
            result = await self.db.execute(query)
            leaderboard = [
                LeaderboardEntry(
                    first_name=row.first_name,
                    total_score=row.total_score,
                    games_played=row.games_played
                )
                for row in result.all()
            ]
            return {"data": leaderboard}


    async def get_user_total(self, user_id: UUID) -> dict:
        """
        Get user's total score and games played.

        Args:
        - user_id (UUID): The user's UUID

        Returns:
        - dict: Total score and games played
        """
        query = select(
            func.sum(GameScore.score).label("total_score"),
            func.count(GameScore.id).label("games_played")
        ).where(
            GameScore.user_id == user_id,
            ~col(GameScore.is_deleted)
        )
        
        result = await self.db.execute(query)
        row = result.one()
        return {
            "total_score": row.total_score or 0,
            "games_played": row.games_played or 0
        }