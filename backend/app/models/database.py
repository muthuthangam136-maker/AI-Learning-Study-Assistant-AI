import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ConversationModel(Base):
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), default="New Study Session")
    subject = Column(String(100), default="General")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("MessageModel", back_populates="conversation", cascade="all, delete-orphan", order_by="MessageModel.created_at")
    goals = relationship("StudyGoalModel", back_populates="conversation", cascade="all, delete-orphan")

class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False) # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    
    # Metadata for agent responses
    intent = Column(String(100), nullable=True)
    topic = Column(String(100), nullable=True)
    status = Column(String(50), default="answered") # answered, learning, needs_teacher
    
    # Structured JSON data
    tools_used = Column(JSON, default=list)
    sources = Column(JSON, default=list)
    activity = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("ConversationModel", back_populates="messages")

class StudyGoalModel(Base):
    __tablename__ = "study_goals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=True)
    subject = Column(String(100), nullable=False)
    topic = Column(String(100), nullable=False)
    target_date = Column(String(50), nullable=True)
    status = Column(String(50), default="in_progress") # in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("ConversationModel", back_populates="goals")

class QuizResultModel(Base):
    __tablename__ = "quiz_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), nullable=True)
    subject = Column(String(100), nullable=False)
    topic = Column(String(100), nullable=False)
    difficulty = Column(String(20), default="Medium")
    total_questions = Column(Integer, default=5)
    score = Column(Integer, default=0)
    percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeDocumentModel(Base):
    __tablename__ = "knowledge_documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False, unique=True)
    subject = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    chunks_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
