import src.auth.models
import src.tasks.models
from src.shared.database import DATABASE_URL, Base
import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ------------------------------------------------------------------------
# 1. Path Setup: Ensure python can find your 'src' folder
# ------------------------------------------------------------------------
sys.path.insert(0, os.path.abspath(os.getcwd()))

# ------------------------------------------------------------------------
# 2. Imports: Bring in Config and Models
# ------------------------------------------------------------------------
# Import DATABASE_URL and Base from the shared dependencies

# CRITICAL: Import your models so they register with Base.metadata
# Even if you don't use 'User' here, importing the file executes the code
# that tells SQLAlchemy "I exist".
# Future models: import src.tasks.models

# ------------------------------------------------------------------------
# 3. Alembic Config Setup
# ------------------------------------------------------------------------
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the metadata so autogenerate works
target_metadata = Base.metadata

# ------------------------------------------------------------------------
# 4. URL Overwrite Logic
# ------------------------------------------------------------------------
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

# Ensure async driver
if not DATABASE_URL.startswith("postgresql+asyncpg"):
    final_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
else:
    final_url = DATABASE_URL

config.set_main_option("sqlalchemy.url", final_url)


# ------------------------------------------------------------------------
# 5. Migration Runners
# ------------------------------------------------------------------------

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())
