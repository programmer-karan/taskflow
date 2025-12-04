import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.main import app
from src.shared.database import Base, get_async_db, DATABASE_URL

# 1. Fixture: Create the Engine & Tables
# Scope = Session means "Do this once per test run"


@pytest.fixture(scope="function")
async def db_engine():
    """
    Creates the Async Engine bound to the correct event loop.
    """
    # Create engine INSIDE the fixture
    engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

    # Create Tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop Tables (Cleanup)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

# 2. Fixture: Get a Test DB Session


@pytest.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Creates a fresh session for each test using the engine above.
    """
    TestingSessionLocal = async_sessionmaker(
        bind=db_engine, expire_on_commit=False)

    async with TestingSessionLocal() as session:
        yield session

# 3. Fixture: The Async HTTP Client


@pytest.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """
    Overrides the dependency so the app uses the TEST session.
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
