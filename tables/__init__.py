import json
from pathlib import Path
from functools import lru_cache
import asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.sql import Insert
from aiopath import AsyncPath

from tables.base import Base
from utils import import_all
from logger import logger
from settings import load_config

settings = load_config()

import_all(__file__, globals(), __package__)  # import all tables


@lru_cache(maxsize=1)
def get_engine(echo=False, **kwargs):
    logger.info("Creating Database Enigne")
    return create_async_engine(
        settings.DB_URL,
        echo=echo,
        **kwargs,
    )


@lru_cache(maxsize=1)
def create_session(engine: AsyncEngine = get_engine()):
    return async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session(LocalSession=create_session()):
    session = LocalSession()
    try:
        yield session
    finally:
        await session.close()


async def create_tables(engine: AsyncEngine = get_engine()):
    logger.info("Creating Database Tables")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine: AsyncEngine = get_engine()):
    logger.info("Dropping Database Tables")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def add_data(data_dir: Path, LocalSession: async_sessionmaker[AsyncSession] = create_session()):
    tables = Base.metadata.tables
    files = AsyncPath(data_dir).glob("*.json")
    queries = []
    async with asyncio.TaskGroup() as tg:
        async def create_and_add_query(file: AsyncPath):
            queries.append(tables[file.stem].insert().values(json.loads(await file.read_bytes())))

        async for file in files:
            tg.create_task(create_and_add_query(file))

    async def execute(query: Insert, session: AsyncSession):
        logger.info(f"\033[48;5;12mAdding Data To:\033[49m {query.table.name} table")
        await session.execute(query)
        await session.commit()
        await session.close()
        logger.info(f"\033[48;5;22mData Added From:\033[49m {query.table.name}.json")

    try:
        async with asyncio.TaskGroup() as tg:
            for query in queries:
                tg.create_task(execute(query, LocalSession()))
    except Exception as e:
        logger.error("\033[48;5;9mCouldn't Execute The Query\033[49m", exc_info=True)
        raise RuntimeError("\033[48;5;9mCouldn't Execute The Query\033[49m") from e
