from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from .config import settings

# 1. Prepare the Async URL for Neon/Postgres
# We ensure the URL uses 'postgresql+asyncpg' for the async engine
async_url = settings.DATABASE_URL
if async_url.startswith("postgres://"):
    async_url = async_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif async_url.startswith("postgresql://"):
    async_url = async_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# 2. Prepare the Sync URL for Table Creation
# SQLModel's create_engine needs 'postgresql' or 'postgres' (without +asyncpg)
sync_url = async_url.replace("+asyncpg", "")

# --- ASYNC ENGINE (For FastAPI Routes) ---
async_engine = create_async_engine(
    async_url,
    echo=True,
    pool_pre_ping=True  # Recommended for Neon to keep connections alive
)

# --- SYNC ENGINE (For Table Creation in main.py) ---
# We remove check_same_thread because it's only for SQLite
sync_engine = create_engine(
    sync_url,
    pool_pre_ping=True
)

# Session generator for your API routes
async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    """Dependency for providing async database sessions to routes."""
    async with async_session_maker() as session:
        yield session