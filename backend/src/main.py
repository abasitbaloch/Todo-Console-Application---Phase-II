"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine
# Use absolute import style for the container
from src.core.config import settings
from src.api import auth, tasks
from src.models import User, Task

# --- DATABASE SETUP ---
# We force a synchronous connection for table creation to avoid Greenlet errors.
# SQLModel.metadata.create_all() does not support async engines.
sync_database_url = settings.DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite://")

engine = create_engine(
    sync_database_url, 
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    """Creates the 'users' and 'tasks' tables in the SQLite file."""
    SQLModel.metadata.create_all(engine)

# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Full-Stack Todo Application API",
    version="1.0.0",
)

# --- STARTUP EVENT ---
@app.on_event("startup")
def on_startup():
    # This runs the second the server starts
    create_db_and_tables()

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows Vercel to communicate with the API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---
@app.get("/")
async def root():
    return {"status": "online", "message": "Backend is running! Visit /docs for API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Router registration
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Backup routes for /api prefix (common for frontend compatibility)
app.include_router(auth.router, prefix="/api/auth", tags=["auth-backup"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks-backup"])