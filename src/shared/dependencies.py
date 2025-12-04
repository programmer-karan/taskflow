import os
from typing import AsyncGenerator
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase

load_dotenv()  # reads .env file

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", "password"))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "taskflow")

DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


DATABASE_URL = os.getenv("DATABASE_URL")


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)


class Base(DeclarativeBase):
    metadata = metadata


engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,  # set True for debugging, switch to False in Prod
    future=True,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # convenient for web apps
    class_=AsyncSession,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Use this as: db: AsyncSession = Depends(get_async_db)
    """
    async with AsyncSessionLocal() as session:
        yield session


# async def create_db_and_tables(Base: DeclarativeBase) -> None:
#     """
#     Run Once (dev) to create all tables from SQLAlchemy models.
#     """

#     async with engine.begin() as conn:
#         # run_sync runs the sync create_all on the sync MetaData

#         await conn.run_sync(Base.metadata.create_all)
