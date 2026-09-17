from typing import Dict, Any, Optional

class DifficultyAssessmentTool:
    name = "Difficulty Assessment Tool"
    description = "Estimates student learning mastery and topic difficulty level based on study queries and quiz accuracy."

    def execute(self, topic: str, accuracy: Optional[float] = None, queries_count: int = 1) -> Dict[str, Any]:
        if accuracy is not None:
            if accuracy >= 80:
                level = "Advanced Mastery"
                recommendation = f"You have demonstrated strong grasp of {topic}. Recommended next step: Solve complex boundary problems and algorithmic implementations."
            elif accuracy >= 50:
                level = "Intermediate / Competent"
                recommendation = f"Solid foundation in {topic} with minor conceptual gaps. Recommended next step: Review missed quiz questions and step-by-step examples."
            else:
                level = "Foundational / Needs Reinforcement"
                recommendation = f"Foundational concepts in {topic} need reinforcement. Recommended next step: Request step-by-step analogies and simpler code walkthroughs."
        else:
            level = "Initial Exploration"
            recommendation = f"Beginning study in {topic}. Start with basic definitions, followed by a 5-question diagnostic quiz."

        return {
            "topic": topic,
            "assessed_level": level,
            "accuracy_score": accuracy,
            "queries_in_session": queries_count,
            "recommendation": recommendation,
            "disclaimer": "Educational diagnostic assessment only; designed to tailor AI explanations."
        }
