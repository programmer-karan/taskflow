import uuid
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.main import app
from src.shared.database import Base, get_async_db, DATABASE_URL

# 1. DATABASE ENGINE (Function Scope)


@pytest.fixture(scope="function")
async def db_engine():
    engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

# 2. DB SESSION


@pytest.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    TestingSessionLocal = async_sessionmaker(
        bind=db_engine, expire_on_commit=False)
    async with TestingSessionLocal() as session:
        yield session

# 3. REDIS CACHE (The Fix)


@pytest.fixture(scope="function", autouse=True)
async def setup_cache():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    await redis.flushdb()  # <--- WIPE CLEAN BEFORE TEST
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache-test")
    yield
    await redis.flushdb()  # <--- WIPE CLEAN AFTER TEST
    await redis.close()

# 4. HTTP CLIENT (Rate Limit Fix)


@pytest.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_db

    # FIX: Generate a RANDOM IP for every test function.
    # This ensures Test A's rate limit doesn't affect Test B.
    fake_ip = f"127.0.{uuid.uuid4().int % 255}.1"

    transport = ASGITransport(app=app, client=(fake_ip, 12345))

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
