from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schemas import ChatRequest, ChatResponse
from app.memory.db import get_db
from app.memory.memory_service import MemoryService
from app.agents.learning_agent import LearningAgent

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
def handle_chat(payload: ChatRequest, db: Session = Depends(get_db)):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Query message cannot be empty.")
        
    memory_service = MemoryService(db)
    
    # Get or create conversation session
    conv = memory_service.get_or_create_conversation(payload.conversation_id)
    
    # Save user message to database
    memory_service.save_message(
        conversation_id=conv.id,
        role="user",
        content=payload.message
    )
    
    # Initialize and execute agent workflow
    agent = LearningAgent(memory_service)
    result = agent.process_message(
        conversation_id=conv.id,
        user_message=payload.message,
        explicit_subject=payload.subject
    )
    
    return result

@router.post("/new")
def start_new_chat(db: Session = Depends(get_db)):
    memory_service = MemoryService(db)
    conv = memory_service.get_or_create_conversation()
    return {
        "conversation_id": conv.id,
        "title": conv.title,
        "created_at": conv.created_at.isoformat()
    }
