"""
$ docker pull postgres
$ docker run --name redin_ecomm -e POSTGRES_PASSWORD=admin -e POSTGRES_USER=redin_admin -e POSTGRES_DB=redin_DB  -d -p 5432:5432 postgres
"""

from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


# TODO: set DB URL based on ENV
DATABASE_URL = "postgresql+asyncpg://postgres:Anu2005$@localhost:5432/doping"

engine = create_async_engine(DATABASE_URL, echo="debug", future=True)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)


async def initiate():
    async with engine.begin() as conn:
        # TODO: remove this after moving to a proper migration setup
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.close()
