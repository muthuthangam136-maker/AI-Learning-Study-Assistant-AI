import os
import sys
import uuid
from pathlib import Path

# Add backend directory to sys.path so app imports work seamlessly
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.config import settings
from app.rag.vector_store import VectorStoreService
from app.memory.db import init_db, SessionLocal
from app.models.database import KnowledgeDocumentModel

SUBJECT_MAP = {
    "dbms.txt": ("DBMS", "Database Management Systems Guide"),
    "data_structures.txt": ("Data Structures", "Data Structures & Algorithms"),
    "operating_systems.txt": ("Operating Systems", "Operating Systems Concepts"),
    "computer_networks.txt": ("Computer Networks", "Computer Networks & Protocols"),
    "java.txt": ("Java", "Java Programming & OOP"),
    "python.txt": ("Python", "Python Language & Techniques"),
    "web_development.txt": ("Web Development", "Web Dev & React Architecture"),
    "software_engineering.txt": ("Software Engineering", "SDLC & Software Engineering"),
    "artificial_intelligence.txt": ("AI", "Artificial Intelligence & Search"),
    "machine_learning.txt": ("Machine Learning", "Machine Learning & Evaluation"),
    "cloud_computing.txt": ("Cloud Computing", "Cloud Computing & Containers"),
    "computer_organization.txt": ("Computer Organization", "Computer Organization & Architecture")
}

def chunk_text(content: str, filename: str, subject: str, doc_title: str):
    """Split text file logically based on markdown section headers or paragraph bounds."""
    chunks = []
    metadatas = []
    ids = []
    
    sections = content.split("\n## ")
    for idx, sec in enumerate(sections):
        lines = sec.strip().split("\n")
        if not lines:
            continue
        
        section_title = lines[0].replace("#", "").strip() if idx > 0 else "Overview"
        text_block = "\n".join(lines).strip()
        
        if len(text_block) < 30:
            continue
            
        chunk_id = f"{filename}_{idx}_{uuid.uuid4().hex[:6]}"
        chunks.append(text_block)
        metadatas.append({
            "title": doc_title,
            "filename": filename,
            "section": section_title,
            "subject": subject
        })
        ids.append(chunk_id)
        
    return chunks, metadatas, ids

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    print("=" * 60)
    print("[AI LEARNING & STUDY ASSISTANT - RAG INGESTION PIPELINE]")
    print("=" * 60)
    
    kb_dir = Path(settings.KNOWLEDGE_BASE_DIR)
    if not kb_dir.exists():
        print(f"❌ Knowledge base directory does not exist: {kb_dir}")
        return
        
    init_db()
    db = SessionLocal()
    vector_service = VectorStoreService.get_instance()
    
    txt_files = list(kb_dir.glob("*.txt"))
    print(f"[INFO] Found {len(txt_files)} educational study documents in {kb_dir}")
    print("-" * 60)
    
    total_indexed_chunks = 0
    
    for file_path in txt_files:
        filename = file_path.name
        subject, doc_title = SUBJECT_MAP.get(
            filename, 
            (filename.replace(".txt", "").replace("_", " ").title(), filename)
        )
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        chunks, metadatas, ids = chunk_text(content, filename, subject, doc_title)
        
        if chunks:
            vector_service.add_chunks(chunks, metadatas, ids)
            total_indexed_chunks += len(chunks)
            
            # Sync to SQLite KnowledgeDocumentModel
            existing_doc = db.query(KnowledgeDocumentModel).filter(
                KnowledgeDocumentModel.filename == filename
            ).first()
            
            desc = f"Study guide for {subject} with {len(chunks)} knowledge modules."
            if not existing_doc:
                new_doc = KnowledgeDocumentModel(
                    id=str(uuid.uuid4()),
                    title=doc_title,
                    filename=filename,
                    subject=subject,
                    description=desc,
                    chunks_count=len(chunks)
                )
                db.add(new_doc)
            else:
                existing_doc.title = doc_title
                existing_doc.subject = subject
                existing_doc.description = desc
                existing_doc.chunks_count = len(chunks)
                
            db.commit()
            print(f"[OK] Indexed [{subject:22}] -> {filename} ({len(chunks)} chunks)")
            
    db.close()
    
    print("-" * 60)
    print(f"[SUCCESS] RAG Ingestion Completed Successfully!")
    print(f"[METRICS] Total Chunks in ChromaDB: {total_indexed_chunks}")
    print(f"[STORAGE] Vector Storage Path:     {settings.CHROMA_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    main()
