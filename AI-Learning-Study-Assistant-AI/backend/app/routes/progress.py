from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.schemas import ProgressStats
from app.memory.db import get_db
from app.memory.memory_service import MemoryService

router = APIRouter(prefix="/api/progress", tags=["Progress"])

@router.get("", response_model=ProgressStats)
def get_progress_dashboard(db: Session = Depends(get_db)):
    """Aggregate learning progress metrics from SQLite memory."""
    memory_service = MemoryService(db)
    stats = memory_service.get_progress_stats()
    return stats
