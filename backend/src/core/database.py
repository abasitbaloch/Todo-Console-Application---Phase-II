from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from .config import settings

# --- ASYNC ENGINE (For FastAPI Routes) ---
# Ensures the URL uses sqlite+aiosqlite://
async_url = settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
async_engine = create_async_engine(
    async_url,
    echo=True,
    connect_args={"check_same_thread": False}
)

# --- SYNC ENGINE (For Table Creation in main.py) ---
# Ensures the URL uses standard sqlite://
sync_url = settings.DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite://")
sync_engine = create_engine(
    sync_url,
    connect_args={"check_same_thread": False}
)

# Session generator for your API routes
async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    """Dependency for providing async database sessions to routes."""
    async with async_session_maker() as session:
        yield session