"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from src.core.config import settings
from src.core.database import sync_engine
from src.api import auth, tasks
from src.models import User, Task

# --- DATABASE TABLE CREATION ---
def create_db_and_tables():
    SQLModel.metadata.create_all(sync_engine)

# --- APP CONFIGURATION ---
# We set redirect_slashes=False to stop the 307 errors
app = FastAPI(
    title="Todo API",
    description="Full-Stack Todo Application API",
    version="1.0.0",
    redirect_slashes=False 
)

# --- STARTUP EVENT ---
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTES ---
@app.get("/")
async def root():
    return {"status": "online"}

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
# Backup prefix
app.include_router(auth.router, prefix="/api/auth", tags=["auth-backup"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks-backup"])