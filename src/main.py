from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from slowapi import Limiter
from src.auth.models import Base
from src.auth.router import router as auth_router
from src.tasks.router import router as task_router
from src.files.router import router as file_router
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend
from src.shared.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# lifespan defination
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

# Attach to App (Not Router!)
app = FastAPI(title="TaskFlow API",lifespan=lifespan)

# Attach to App 
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app = FastAPI(tiltle="Taskflow API")


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# include the router
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(file_router)

@app.get("/")
def root():
    return {"message": "The server is working!"}