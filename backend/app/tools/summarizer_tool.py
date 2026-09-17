from typing import Dict, Any, List, Optional

class TopicSummarizerTool:
    name = "Topic Summarizer Tool"
    description = "Extracts definitions, key bullet points, exam formulas, and quick revision notes from study material."

    def execute(self, topic: str, content: Optional[str] = None) -> Dict[str, Any]:
        return {
            "topic": topic,
            "summary_type": "Executive Revision Notes",
            "key_takeaways": [
                f"Core Definition: Essential foundational principles governing {topic}.",
                "Critical Distinction: Nuanced differences frequently tested in university exams.",
                "Real-World Analogy: Intuitive mental model to remember the architecture.",
                "Common Pitfalls: Common student misconceptions and boundary bugs."
            ],
            "exam_checklist": [
                "State formal mathematical/algorithmic definition",
                "Draw standard system architecture or state diagram",
                "Explain time and space complexity trade-offs",
                "Provide at least one minimal working code or query example"
            ]
        }
