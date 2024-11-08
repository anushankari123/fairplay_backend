from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.misc import get_session


class BaseService:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db
