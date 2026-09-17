from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class ActivityStep(BaseModel):
    step: str
    status: str = "completed" # pending, in_progress, completed, warning
    detail: Optional[str] = None

class SourceItem(BaseModel):
    title: str
    filename: str
    section: Optional[str] = "General"
    relevance: float = 0.85
    excerpt: Optional[str] = None

class ToolExecutionResult(BaseModel):
    tool_name: str
    action: str
    result: Any
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Student's query or instruction")
    conversation_id: Optional[str] = None
    subject: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    intent: str
    topic: str
    status: str # answered, learning, needs_teacher
    tools_used: List[ToolExecutionResult] = []
    sources: List[SourceItem] = []
    activity: List[ActivityStep] = []
    memory_updated: bool = True
    suggested_followups: List[str] = []
    created_at: str

class MessageItem(BaseModel):
    id: str
    role: str
    content: str
    intent: Optional[str] = None
    topic: Optional[str] = None
    status: Optional[str] = None
    tools_used: List[Any] = []
    sources: List[Any] = []
    activity: List[Any] = []
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationSummary(BaseModel):
    id: str
    title: str
    subject: str
    message_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ConversationDetail(BaseModel):
    id: str
    title: str
    subject: str
    messages: List[MessageItem]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class QuizPayload(BaseModel):
    subject: str
    topic: str
    difficulty: str = "Medium"
    questions: List[QuizQuestion]

class QuizSubmitRequest(BaseModel):
    conversation_id: Optional[str] = None
    subject: str
    topic: str
    difficulty: str
    total_questions: int
    score: int

class StudyPlanDay(BaseModel):
    day: int
    focus_topic: str
    duration_hours: float
    activities: List[str]

class StudyPlanPayload(BaseModel):
    subject: str
    days: int
    daily_hours: float
    plan: List[StudyPlanDay]
    tips: List[str]

class KnowledgeDocCreate(BaseModel):
    title: str
    filename: str
    subject: str
    description: Optional[str] = ""
    content: str

class KnowledgeDocSummary(BaseModel):
    id: str
    title: str
    filename: str
    subject: str
    description: Optional[str] = ""
    chunks_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProgressStats(BaseModel):
    topics_studied_count: int
    questions_asked_count: int
    quizzes_completed_count: int
    average_quiz_score: float
    study_sessions_count: int
    recent_activity: List[Dict[str, Any]]
    subject_breakdown: Dict[str, int]
