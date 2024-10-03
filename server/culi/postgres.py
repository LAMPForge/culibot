from typing import TypeAlias, Literal
from collections.abc import AsyncGenerator
from fastapi import Depends, Request
from culi.common.db.postgres import (
    AsyncEngine,
    AsyncSession,
    AsyncSessionMaker,
    Engine,
    sql,
)
from culi.config import settings
from culi.common.db.postgres import (
    create_async_engine as _create_async_engine,
)
from culi.common.db.postgres import (
    create_sync_engine as _create_sync_engine,
)

ProcessName: TypeAlias = Literal["main", "script"]


def create_async_engine(process_name: ProcessName) -> AsyncEngine:
    return _create_async_engine(
        dsn=str(settings.get_postgres_dsn("asyncpg")),
        application_name=f"{settings.ENV.value}.{process_name}",
        debug=settings.DEBUG,
        pool_size=settings.DATABASE_POOL_SIZE,
        pool_recycle=settings.DATABASE_POOL_RECYCLE_SECONDS,
    )


def create_sync_engine(process_name: ProcessName) -> Engine:
    return _create_sync_engine(
        dsn=str(settings.get_postgres_dsn("psycopg2")),
        application_name=f"{settings.ENV.value}.{process_name}",
        debug=settings.DEBUG,
        pool_size=settings.DATABASE_SYNC_POOL_SIZE,
        pool_recycle=settings.DATABASE_POOL_RECYCLE_SECONDS,
    )


async def get_db_sessionmaker(
    request: Request,
) -> AsyncGenerator[AsyncSessionMaker, None]:
    async_sessionmaker: AsyncSessionMaker = request.state.async_sessionmaker
    yield async_sessionmaker


async def get_db_session(
    request: Request,
    sessionmaker: AsyncSessionMaker = Depends(get_db_sessionmaker),
) -> AsyncGenerator[AsyncSession, None]:
    if session := getattr(request.state, "session", None):
        yield session
    else:
        async with sessionmaker() as session:
            try:
                request.state.session = session
                yield session
            except:
                await session.rollback()
                raise
            else:
                await session.commit()


__all__ = [
    "AsyncSession",
    "sql",
    "create_async_engine",
    "create_sync_engine",
    "get_db_session",
    "get_db_sessionmaker",
]
