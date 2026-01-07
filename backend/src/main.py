"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings

# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Phase II Full-Stack Todo Application API",
    version="1.0.0",
)

# --- CORS CONFIGURATION ---
origins = [
    "http://localhost:3000",
    "https://your-app-name.vercel.app", # Replace with your actual Vercel link
]

# Add settings origins if they exist
if hasattr(settings, "cors_origins_list"):
    origins.extend(settings.cors_origins_list)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HEALTH CHECK ---
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Todo API is running"}


# --- ROUTER REGISTRATION (The "Universal" Fix) ---
from .api import auth, tasks

# 1. Listen at root paths (e.g., http://localhost:8000/auth/login)
# This matches the api.ts code I gave you earlier.
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# 2. ALSO Listen at /api paths (e.g., http://localhost:8000/api/auth/login)
# This acts as a backup in case your frontend is using the /api prefix.
app.include_router(auth.router, prefix="/api/auth", tags=["auth-backup"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks-backup"])