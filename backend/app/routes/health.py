from fastapi import APIRouter
from app.config import settings
from app.rag.vector_store import VectorStoreService

router = APIRouter(tags=["Health"])

@router.get("/api/health")
def health_check():
    vector_store = VectorStoreService.get_instance()
    stats = vector_store.get_stats()
    
    is_real_ai = (not settings.DEMO_MODE) and bool(settings.OPENAI_API_KEY) and settings.OPENAI_API_KEY != "your_openai_api_key_here"

    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "demo_mode": settings.DEMO_MODE,
        "operational_mode": "REAL AI MODE" if is_real_ai else "DEMO MODE",
        "llm_model": settings.LLM_MODEL if is_real_ai else "Built-in Demonstrator",
        "chroma_chunks": stats["total_chunks"],
        "vector_store_active": True,
        "agentic_workflow": "Active"
    }
