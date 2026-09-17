import os
import uuid
from typing import List
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.config import settings
from app.models.database import KnowledgeDocumentModel
from app.models.schemas import KnowledgeDocSummary, KnowledgeDocCreate
from app.memory.db import get_db
from app.rag.vector_store import VectorStoreService

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge Base"])

@router.get("", response_model=List[KnowledgeDocSummary])
def list_knowledge_documents(db: Session = Depends(get_db)):
    docs = db.query(KnowledgeDocumentModel).order_by(KnowledgeDocumentModel.title.asc()).all()
    return docs

@router.post("", response_model=KnowledgeDocSummary)
def add_knowledge_document(payload: KnowledgeDocCreate, db: Session = Depends(get_db)):
    # Validate filename
    clean_filename = os.path.basename(payload.filename)
    if not clean_filename.endswith(".txt"):
        clean_filename += ".txt"
        
    existing = db.query(KnowledgeDocumentModel).filter(KnowledgeDocumentModel.filename == clean_filename).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Document '{clean_filename}' already exists.")

    # Save to knowledge_base directory
    save_path = Path(settings.KNOWLEDGE_BASE_DIR) / clean_filename
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(payload.content)

    # Chunk and index into ChromaDB
    from scripts.ingest import chunk_text
    chunks, metadatas, ids = chunk_text(payload.content, clean_filename, payload.subject, payload.title)
    
    vector_store = VectorStoreService.get_instance()
    if chunks:
        vector_store.add_chunks(chunks, metadatas, ids)

    # Record in DB
    new_doc = KnowledgeDocumentModel(
        id=str(uuid.uuid4()),
        title=payload.title,
        filename=clean_filename,
        subject=payload.subject,
        description=payload.description or f"User study notes for {payload.subject}",
        chunks_count=len(chunks)
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

@router.delete("/{id}")
def delete_knowledge_document(id: str, db: Session = Depends(get_db)):
    doc = db.query(KnowledgeDocumentModel).filter(KnowledgeDocumentModel.id == id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    # Remove file from disk
    file_path = Path(settings.KNOWLEDGE_BASE_DIR) / doc.filename
    if file_path.exists():
        try:
            os.remove(file_path)
        except Exception:
            pass

    # Delete chunks from ChromaDB
    vector_store = VectorStoreService.get_instance()
    vector_store.delete_by_filename(doc.filename)

    # Delete from DB
    db.delete(doc)
    db.commit()
    return {"message": f"Document '{doc.title}' deleted successfully."}
