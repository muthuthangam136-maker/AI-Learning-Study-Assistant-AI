import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.memory.db import init_db
from app.routes import chat, conversations, knowledge, tools, progress, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite tables on startup
    init_db()
    print("==================================================")
    print("[AI LEARNING & STUDY ASSISTANT API SERVER]")
    print(f"[STATUS] Active on port {settings.BACKEND_PORT}")
    print(f"[MODE]   {'DEMO MODE' if settings.DEMO_MODE else 'REAL AI MODE'}")
    print(f"[DOCS]   http://localhost:{settings.BACKEND_PORT}/docs")
    print("==================================================")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Agentic AI Learning & Study Assistant with RAG, Educational Tools, and Conversation Memory.",
    lifespan=lifespan
)

# CORS Configuration for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(conversations.router)
app.include_router(knowledge.router)
app.include_router(tools.router)
app.include_router(progress.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True
    )
