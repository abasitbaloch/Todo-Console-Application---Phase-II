"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine
# Use absolute import style for the container
from src.core.config import settings
from src.api import auth, tasks
from src.models import User, Task

# --- DATABASE AUTO-CREATION ---
# Create the engine for the writable /tmp/ directory
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# This creates the 'users' and 'tasks' tables on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Phase II Full-Stack Todo Application API",
    version="1.0.0",
)

# --- STARTUP EVENT ---
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows Vercel to communicate with Hugging Face
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HOME ROUTE ---
@app.get("/")
async def root():
    return {"status": "online", "message": "Backend is running! Try /docs for API"}

# --- HEALTH CHECK ---
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Todo API is running"}

# --- ROUTER REGISTRATION ---
# Standard routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Backup routes for /api prefix
app.include_router(auth.router, prefix="/api/auth", tags=["auth-backup"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks-backup"])