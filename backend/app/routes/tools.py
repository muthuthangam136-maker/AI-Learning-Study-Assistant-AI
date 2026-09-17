from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.tools.registry import registry
from app.models.schemas import QuizSubmitRequest
from app.memory.db import get_db
from app.memory.memory_service import MemoryService

router = APIRouter(prefix="/api/tools", tags=["Tools"])

@router.get("")
def list_tools():
    """Return all available educational tools in the agent's toolbox."""
    return registry.get_available_tools()

@router.post("/quiz/submit")
def submit_quiz_score(payload: QuizSubmitRequest, db: Session = Depends(get_db)):
    """Record student quiz score in SQLite progress memory."""
    memory_service = MemoryService(db)
    result = memory_service.record_quiz_score(
        conversation_id=payload.conversation_id,
        subject=payload.subject,
        topic=payload.topic,
        difficulty=payload.difficulty,
        total=payload.total_questions,
        score=payload.score
    )
    return {
        "message": "Quiz result recorded in learning memory.",
        "id": result.id,
        "score": result.score,
        "total": result.total_questions,
        "percentage": result.percentage
    }
