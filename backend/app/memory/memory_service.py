import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import ConversationModel, MessageModel, StudyGoalModel, QuizResultModel, KnowledgeDocumentModel

class MemoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_conversation(self, conversation_id: Optional[str] = None, title: Optional[str] = None) -> ConversationModel:
        if conversation_id:
            conv = self.db.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()
            if conv:
                return conv
        
        # Create new conversation
        conv = ConversationModel(
            id=conversation_id or str(uuid.uuid4()),
            title=title or "New Study Session",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv

    def get_recent_history(self, conversation_id: str, limit: int = 6) -> List[Dict[str, str]]:
        """Retrieve recent conversation history formatted for LLM context."""
        messages = self.db.query(MessageModel).filter(
            MessageModel.conversation_id == conversation_id
        ).order_by(MessageModel.created_at.desc()).limit(limit).all()
        
        # Return in chronological order
        history = []
        for m in reversed(messages):
            history.append({
                "role": m.role,
                "content": m.content
            })
        return history

    def get_conversation_context(self, conversation_id: str) -> Dict[str, Any]:
        """Extract learned context (current topic, last goals, recent scores) from memory."""
        messages = self.db.query(MessageModel).filter(
            MessageModel.conversation_id == conversation_id
        ).order_by(MessageModel.created_at.desc()).limit(5).all()

        last_topic = None
        last_intent = None
        for m in messages:
            if m.topic and not last_topic:
                last_topic = m.topic
            if m.intent and not last_intent:
                last_intent = m.intent

        goals = self.db.query(StudyGoalModel).filter(
            StudyGoalModel.conversation_id == conversation_id
        ).order_by(StudyGoalModel.created_at.desc()).limit(3).all()

        return {
            "last_topic": last_topic,
            "last_intent": last_intent,
            "active_goals": [{"subject": g.subject, "topic": g.topic, "status": g.status} for g in goals]
        }

    def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        intent: Optional[str] = None,
        topic: Optional[str] = None,
        status: str = "answered",
        tools_used: Optional[List[Any]] = None,
        sources: Optional[List[Any]] = None,
        activity: Optional[List[Any]] = None
    ) -> MessageModel:
        msg = MessageModel(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content,
            intent=intent,
            topic=topic,
            status=status,
            tools_used=tools_used or [],
            sources=sources or [],
            activity=activity or [],
            created_at=datetime.utcnow()
        )
        self.db.add(msg)
        
        # Update conversation timestamp & title if first message
        conv = self.db.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()
        if conv:
            conv.updated_at = datetime.utcnow()
            if conv.title == "New Study Session" and role == "user":
                # Create a concise title from first query
                clean_title = content.strip().split("\n")[0][:45]
                conv.title = clean_title if clean_title else "Study Session"
            if topic and conv.subject == "General":
                conv.subject = topic
        
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def record_study_goal(self, conversation_id: str, subject: str, topic: str, target_date: Optional[str] = None):
        goal = StudyGoalModel(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            subject=subject,
            topic=topic,
            target_date=target_date,
            status="in_progress",
            created_at=datetime.utcnow()
        )
        self.db.add(goal)
        self.db.commit()
        return goal

    def record_quiz_score(self, conversation_id: Optional[str], subject: str, topic: str, difficulty: str, total: int, score: int):
        pct = (score / total * 100.0) if total > 0 else 0.0
        result = QuizResultModel(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            subject=subject,
            topic=topic,
            difficulty=difficulty,
            total_questions=total,
            score=score,
            percentage=pct,
            created_at=datetime.utcnow()
        )
        self.db.add(result)
        self.db.commit()
        return result

    def get_progress_stats(self) -> Dict[str, Any]:
        # Count user questions asked
        questions_count = self.db.query(MessageModel).filter(MessageModel.role == "user").count()
        sessions_count = self.db.query(ConversationModel).count()
        quizzes = self.db.query(QuizResultModel).all()
        quizzes_count = len(quizzes)
        avg_score = (sum(q.percentage for q in quizzes) / quizzes_count) if quizzes_count > 0 else 0.0

        # Unique topics studied
        topic_counts = self.db.query(MessageModel.topic, func.count(MessageModel.id)).filter(
            MessageModel.topic != None,
            MessageModel.topic != "Other"
        ).group_by(MessageModel.topic).all()

        subject_breakdown = {t[0]: t[1] for t in topic_counts}
        topics_studied_count = len(subject_breakdown)

        # Recent activities
        recent_messages = self.db.query(MessageModel).filter(
            MessageModel.role == "assistant"
        ).order_by(MessageModel.created_at.desc()).limit(6).all()

        recent_activity = []
        for m in recent_messages:
            recent_activity.append({
                "id": m.id,
                "topic": m.topic or "Study Query",
                "intent": m.intent or "Discussion",
                "status": m.status,
                "date": m.created_at.strftime("%b %d, %Y %H:%M")
            })

        return {
            "topics_studied_count": topics_studied_count,
            "questions_asked_count": questions_count,
            "quizzes_completed_count": quizzes_count,
            "average_quiz_score": round(avg_score, 1),
            "study_sessions_count": sessions_count,
            "recent_activity": recent_activity,
            "subject_breakdown": subject_breakdown
        }
