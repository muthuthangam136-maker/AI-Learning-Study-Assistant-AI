from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import ConversationModel, MessageModel
from app.models.schemas import ConversationSummary, ConversationDetail
from app.memory.db import get_db

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])

@router.get("", response_model=List[ConversationSummary])
def list_conversations(db: Session = Depends(get_db)):
    conversations = db.query(ConversationModel).order_by(ConversationModel.updated_at.desc()).all()
    summaries = []
    for c in conversations:
        msg_count = db.query(MessageModel).filter(MessageModel.conversation_id == c.id).count()
        summaries.append(
            ConversationSummary(
                id=c.id,
                title=c.title,
                subject=c.subject,
                message_count=msg_count,
                created_at=c.created_at,
                updated_at=c.updated_at
            )
        )
    return summaries

@router.get("/{id}", response_model=ConversationDetail)
def get_conversation(id: str, db: Session = Depends(get_db)):
    conv = db.query(ConversationModel).filter(ConversationModel.id == id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation session not found.")
    return conv

@router.delete("/{id}")
def delete_conversation(id: str, db: Session = Depends(get_db)):
    conv = db.query(ConversationModel).filter(ConversationModel.id == id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation session not found.")
    db.delete(conv)
    db.commit()
    return {"message": "Conversation session deleted successfully."}
