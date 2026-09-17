from typing import Dict, Any, List, Optional
from app.rag.vector_store import VectorStoreService

class StudySearchTool:
    name = "Study Material Search Tool"
    description = "Searches the ChromaDB knowledge base for relevant concepts, definitions, and formulas."

    def execute(self, query: str, topic: Optional[str] = None, n_results: int = 3) -> Dict[str, Any]:
        vector_store = VectorStoreService.get_instance()
        results = vector_store.search(query=query, topic=topic, n_results=n_results)
        
        sources_summary = [
            {
                "title": r["title"],
                "filename": r["filename"],
                "section": r["section"],
                "relevance": r["relevance"],
                "excerpt": r["excerpt"]
            }
            for r in results
        ]
        
        return {
            "query": query,
            "topic": topic or "General",
            "matches_found": len(results),
            "sources": sources_summary,
            "combined_context": "\n\n".join([f"[{r['filename']} - {r['section']}]: {r['full_text']}" for r in results])
        }
