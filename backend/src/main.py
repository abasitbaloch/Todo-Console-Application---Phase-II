"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Use absolute import style for the container
from src.core.config import settings
from src.api import auth, tasks

# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Phase II Full-Stack Todo Application API",
    version="1.0.0",
)

# --- CORS CONFIGURATION ---
# We take the origins directly from your Hugging Face Secret
origins = settings.CORS_ORIGINS if hasattr(settings, "CORS_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For testing, we allow all. We can tighten this later.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HOME ROUTE (To fix the 404) ---
@app.get("/")
async def root():
    return {"status": "online", "message": "Backend is running! Try /docs for API"}

# --- HEALTH CHECK ---
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Todo API is running"}

# --- ROUTER REGISTRATION ---
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth-backup"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks-backup"])