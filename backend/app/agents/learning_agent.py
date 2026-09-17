import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from app.config import settings
from app.memory.memory_service import MemoryService
from app.rag.vector_store import VectorStoreService
from app.agents.classifier import classify_intent_and_subject
from app.agents.demo_data import get_demo_response
from app.tools.study_search_tool import StudySearchTool
from app.tools.quiz_tool import QuizGeneratorTool
from app.tools.study_plan_tool import StudyPlanTool
from app.tools.summarizer_tool import TopicSummarizerTool
from app.tools.assessment_tool import DifficultyAssessmentTool

class LearningAgent:
    def __init__(self, memory_service: MemoryService):
        self.memory = memory_service
        self.vector_store = VectorStoreService.get_instance()
        self.search_tool = StudySearchTool()
        self.quiz_tool = QuizGeneratorTool()
        self.plan_tool = StudyPlanTool()
        self.summarizer_tool = TopicSummarizerTool()
        self.assessment_tool = DifficultyAssessmentTool()

    def process_message(
        self,
        conversation_id: str,
        user_message: str,
        explicit_subject: Optional[str] = None
    ) -> Dict[str, Any]:
        """Executes the autonomous 7-stage Agentic AI Workflow."""
        activity = []
        tools_used = []
        
        # 1. Understand Student Request & Step 1 Activity
        activity.append({
            "step": "Learning request analyzed",
            "status": "completed",
            "detail": f"Length: {len(user_message)} characters"
        })

        # 2. Intent and Topic Classification
        context = self.memory.get_conversation_context(conversation_id)
        intent, subject = classify_intent_and_subject(
            user_message,
            previous_topic=context.get("last_topic")
        )
        if explicit_subject and explicit_subject != "General":
            subject = explicit_subject

        activity.append({
            "step": "Intent classified",
            "status": "completed",
            "detail": intent
        })
        activity.append({
            "step": "Topic identified",
            "status": "completed",
            "detail": subject
        })

        # 3. RAG Knowledge Search
        retrieved_sources = []
        rag_results = self.vector_store.search(
            query=user_message,
            topic=subject if subject != "Other" else None,
            n_results=3
        )

        activity.append({
            "step": "Knowledge base searched",
            "status": "completed",
            "detail": f"Indexed collection: {self.vector_store.collection_name}"
        })

        if rag_results:
            for r in rag_results:
                retrieved_sources.append({
                    "title": r["title"],
                    "filename": r["filename"],
                    "section": r["section"],
                    "relevance": r["relevance"],
                    "excerpt": r["excerpt"]
                })
            activity.append({
                "step": "Relevant study material retrieved",
                "status": "completed",
                "detail": f"Retrieved {len(retrieved_sources)} relevant chunk(s)"
            })
        else:
            activity.append({
                "step": "Knowledge search completed",
                "status": "completed",
                "detail": "General knowledge retrieval applied"
            })

        # 4. Decide Whether Educational Tool is Required
        tool_selected = None
        tool_detail = "No external tool required"

        if intent == "Quiz":
            tool_selected = "quiz"
            tool_detail = "Quiz Generator Tool selected"
        elif intent == "Study Plan" or ("exam" in user_message.lower() and any(w in user_message.lower() for w in ["days", "plan", "prepare", "schedule"])):
            tool_selected = "plan"
            tool_detail = "Study Plan Generator Tool selected"
        elif intent == "Summarization":
            tool_selected = "summarizer"
            tool_detail = "Topic Summarizer Tool selected"
        elif intent == "Progress Review":
            tool_selected = "assessment"
            tool_detail = "Difficulty Assessment Tool selected"

        activity.append({
            "step": "Tool selection decision",
            "status": "completed",
            "detail": tool_detail
        })

        # 5. Tool Execution
        tool_result = None
        if tool_selected == "quiz":
            target_sub = subject if subject != "Other" else "DBMS"
            tool_result = self.quiz_tool.execute(subject=target_sub, count=5)
            tools_used.append({
                "tool_name": self.quiz_tool.name,
                "action": f"Generated 5 multiple choice questions for {target_sub}",
                "result": tool_result,
                "timestamp": datetime.utcnow().strftime("%H:%M:%S")
            })
            activity.append({
                "step": "Tool executed",
                "status": "completed",
                "detail": f"{self.quiz_tool.name} successfully executed"
            })

        elif tool_selected == "plan":
            target_sub = subject if subject != "Other" else "DBMS"
            # Parse days if provided
            days = 5
            for word in user_message.split():
                if word.isdigit() and 1 <= int(word) <= 30:
                    days = int(word)
                    break
            tool_result = self.plan_tool.execute(subject=target_sub, days=days, daily_hours=2.5)
            tools_used.append({
                "tool_name": self.plan_tool.name,
                "action": f"Generated {days}-day study plan for {target_sub}",
                "result": tool_result,
                "timestamp": datetime.utcnow().strftime("%H:%M:%S")
            })
            activity.append({
                "step": "Tool executed",
                "status": "completed",
                "detail": f"{self.plan_tool.name} successfully executed"
            })

        elif tool_selected == "summarizer":
            tool_result = self.summarizer_tool.execute(topic=subject)
            tools_used.append({
                "tool_name": self.summarizer_tool.name,
                "action": f"Summarized core exam notes for {subject}",
                "result": tool_result,
                "timestamp": datetime.utcnow().strftime("%H:%M:%S")
            })
            activity.append({
                "step": "Tool executed",
                "status": "completed",
                "detail": f"{self.summarizer_tool.name} successfully executed"
            })

        elif tool_selected == "assessment":
            tool_result = self.assessment_tool.execute(topic=subject)
            tools_used.append({
                "tool_name": self.assessment_tool.name,
                "action": f"Assessed mastery for {subject}",
                "result": tool_result,
                "timestamp": datetime.utcnow().strftime("%H:%M:%S")
            })
            activity.append({
                "step": "Tool executed",
                "status": "completed",
                "detail": f"{self.assessment_tool.name} successfully executed"
            })

        # 6. Check Teacher Assistance Condition
        status = "answered"
        # If query is completely off-topic or nonsensical and no sources matched
        if len(user_message.strip().split()) > 3 and not rag_results and subject == "Other" and intent == "Other":
            status = "needs_teacher"

        # 7. Generate Personalized Grounded Response
        final_message = ""
        suggested_followups = []

        is_real_ai_active = (not settings.DEMO_MODE) and bool(settings.OPENAI_API_KEY) and settings.OPENAI_API_KEY != "your_openai_api_key_here"

        if is_real_ai_active:
            try:
                final_message, followups = self._generate_llm_response(
                    user_message=user_message,
                    intent=intent,
                    subject=subject,
                    rag_sources=retrieved_sources,
                    tool_result=tool_result,
                    conversation_id=conversation_id
                )
                suggested_followups = followups
            except Exception as e:
                print(f"LLM generation warning: {e}. Falling back to safe response.")
                demo = get_demo_response(user_message, intent, subject)
                final_message = demo["message"]
                suggested_followups = demo.get("suggested_followups", [])
        else:
            # DEMO MODE
            demo = get_demo_response(user_message, intent, subject)
            final_message = demo["message"]
            if not tools_used and demo.get("tools_used"):
                tools_used = demo["tools_used"]
            if not retrieved_sources and demo.get("sources"):
                retrieved_sources = demo["sources"]
            suggested_followups = demo.get("suggested_followups", [])

        # If Teacher assistance was flagged
        if status == "needs_teacher":
            final_message += "\n\n> ⚠️ **Teacher Assistance Recommended:**\n> Based on the available knowledge base, there is insufficient material to provide a complete verified answer. Please consult your course instructor or lecturer for official syllabus clarification."

        # 8. Memory Update
        activity.append({
            "step": "Memory updated",
            "status": "completed",
            "detail": "Conversation session and learned goals updated"
        })

        # Record study goal in memory if study plan was generated
        if tool_selected == "plan":
            self.memory.record_study_goal(conversation_id, subject=subject, topic=f"{subject} Exam Prep")

        # Save assistant message in SQLite
        self.memory.save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=final_message,
            intent=intent,
            topic=subject,
            status=status,
            tools_used=tools_used,
            sources=retrieved_sources,
            activity=activity
        )

        activity.append({
            "step": "Final response generated",
            "status": "completed",
            "detail": "Delivered to student"
        })

        return {
            "conversation_id": conversation_id,
            "message": final_message,
            "intent": intent,
            "topic": subject,
            "status": status,
            "tools_used": tools_used,
            "sources": retrieved_sources,
            "activity": activity,
            "memory_updated": True,
            "suggested_followups": suggested_followups,
            "created_at": datetime.utcnow().isoformat()
        }

    def _generate_llm_response(
        self,
        user_message: str,
        intent: str,
        subject: str,
        rag_sources: List[Dict[str, Any]],
        tool_result: Optional[Dict[str, Any]],
        conversation_id: str
    ) -> Tuple[str, List[str]]:
        from openai import OpenAI
        
        client_kwargs = {"api_key": settings.OPENAI_API_KEY}
        if settings.LLM_BASE_URL:
            client_kwargs["base_url"] = settings.LLM_BASE_URL
        client = OpenAI(**client_kwargs)

        # Build grounded context
        context_str = "\n\n".join([f"[Source: {s['filename']} - {s.get('section', 'General')}]:\n{s.get('excerpt', '')}" for s in rag_sources])
        
        system_prompt = f"""You are the 'AI Learning & Study Assistant', a warm, expert computer science tutor built for the IBM/TNSDC Agentic AI internship.
Your goal is to guide students with clear, beginner-friendly explanations, step-by-step breakdowns, code examples where relevant, and active recall practice.

Current Student Request Context:
- Classified Intent: {intent}
- Subject/Topic: {subject}

Grounded Knowledge Base Material:
{context_str if context_str else "No direct document chunks retrieved. Rely on core computer science foundations."}

Tool Execution Result:
{str(tool_result) if tool_result else "None"}

Guidelines:
1. Explain concepts step-by-step with real-world analogies.
2. If programming question: provide clean code, explain key lines, and mention common pitfalls.
3. Structure your answer with clear markdown headers: Topic, Simple Explanation, Step-by-Step Breakdown, Example/Code, Key Takeaways, Practice.
4. End with a helpful follow-up question or practice exercise.
5. If the user question cannot be reliably answered from CS foundations, politely advise consulting a lecturer.
"""
        history = self.memory.get_recent_history(conversation_id, limit=4)
        messages = [{"role": "system", "content": system_prompt}]
        for h in history:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            temperature=0.4,
            max_tokens=1500
        )
        content = response.choices[0].message.content or "I have processed your study request."
        
        # Follow-ups
        followups = [
            f"Quiz me on {subject}",
            f"Create a study plan for {subject}",
            "Explain with another example"
        ]
        return content, followups
