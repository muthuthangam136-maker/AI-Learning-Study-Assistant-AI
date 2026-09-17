from typing import Dict, Any, List
from app.tools.study_search_tool import StudySearchTool
from app.tools.quiz_tool import QuizGeneratorTool
from app.tools.study_plan_tool import StudyPlanTool
from app.tools.summarizer_tool import TopicSummarizerTool
from app.tools.assessment_tool import DifficultyAssessmentTool

class ToolRegistry:
    def __init__(self):
        self.search_tool = StudySearchTool()
        self.quiz_tool = QuizGeneratorTool()
        self.plan_tool = StudyPlanTool()
        self.summarizer_tool = TopicSummarizerTool()
        self.assessment_tool = DifficultyAssessmentTool()

    def get_available_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "study_search",
                "name": self.search_tool.name,
                "icon": "📚",
                "description": self.search_tool.description,
                "inputs": ["query", "topic", "n_results"],
                "output": "Ranked study chunks with cosine similarity and document filenames",
                "status": "active"
            },
            {
                "id": "quiz_generator",
                "name": self.quiz_tool.name,
                "icon": "📝",
                "description": self.quiz_tool.description,
                "inputs": ["subject", "topic", "difficulty", "count"],
                "output": "Multiple choice questions with correct answers, distractor options, and explanations",
                "status": "active"
            },
            {
                "id": "study_plan",
                "name": self.plan_tool.name,
                "icon": "📅",
                "description": self.plan_tool.description,
                "inputs": ["subject", "days", "daily_hours", "weak_topics"],
                "output": "Customized day-by-day study schedule with hour allocations and high-yield activities",
                "status": "active"
            },
            {
                "id": "topic_summarizer",
                "name": self.summarizer_tool.name,
                "icon": "📖",
                "description": self.summarizer_tool.description,
                "inputs": ["topic", "content"],
                "output": "Concise key points, exam revision checklist, and architectural takeaway summary",
                "status": "active"
            },
            {
                "id": "difficulty_assessment",
                "name": self.assessment_tool.name,
                "icon": "📊",
                "description": self.assessment_tool.description,
                "inputs": ["topic", "accuracy", "queries_count"],
                "output": "Learning mastery level (Foundational, Intermediate, Advanced) and tailored next steps",
                "status": "active"
            }
        ]

registry = ToolRegistry()
