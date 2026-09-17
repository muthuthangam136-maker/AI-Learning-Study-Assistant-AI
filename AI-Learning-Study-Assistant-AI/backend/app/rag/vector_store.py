import os
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings

class SimpleHashEmbeddingFunction:
    """Lightweight deterministic local embedding function fallback for immediate zero-dependency initialization."""
    def __call__(self, input: List[str]) -> List[List[float]]:
        embeddings = []
        for text in input:
            vec = [0.0] * 64
            clean = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
            words = clean.split()
            for i, word in enumerate(words):
                h = abs(hash(word)) % 64
                vec[h] += 1.0 / (1.0 + i * 0.05)
            # Normalize
            norm = sum(x * x for x in vec) ** 0.5
            if norm > 0:
                vec = [x / norm for x in vec]
            embeddings.append(vec)
        return embeddings

class VectorStoreService:
    _instance = None

    def __init__(self):
        self.chroma_path = settings.CHROMA_PATH
        os.makedirs(self.chroma_path, exist_ok=True)
        
        # Initialize Persistent Client
        self.client = chromadb.PersistentClient(path=self.chroma_path)
        
        # Try loading sentence-transformers embedding function, fallback gracefully
        self.embedding_fn = None
        try:
            from chromadb.utils import embedding_functions
            self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=settings.EMBEDDING_MODEL
            )
        except Exception:
            try:
                # Default Chroma embedding function if available
                self.embedding_fn = SimpleHashEmbeddingFunction()
            except Exception:
                self.embedding_fn = SimpleHashEmbeddingFunction()

        # Get or create collection
        self.collection_name = "study_knowledge_base"
        try:
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_fn,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception:
            # Fallback collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = VectorStoreService()
        return cls._instance

    def search(self, query: str, topic: Optional[str] = None, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search ChromaDB collection for top-K relevant study chunks."""
        try:
            count = self.collection.count()
            if count == 0:
                return []

            where_filter = None
            if topic and topic.lower() != "other" and topic.lower() != "general":
                where_filter = {"subject": topic}

            # If filtered search yields results, use it; otherwise broaden search
            query_kwargs = {
                "query_texts": [query],
                "n_results": min(n_results, count),
                "include": ["documents", "metadatas", "distances"]
            }
            if where_filter:
                try:
                    results = self.collection.query(where=where_filter, **query_kwargs)
                    if results and results.get("documents") and len(results["documents"][0]) > 0:
                        return self._format_results(results)
                except Exception:
                    pass

            # Unfiltered query
            results = self.collection.query(**query_kwargs)
            return self._format_results(results)
        except Exception as e:
            print(f"Vector search warning: {e}")
            return []

    def _format_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        formatted = []
        if not results or "documents" not in results or not results["documents"]:
            return formatted

        docs = results["documents"][0]
        metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
        distances = results["distances"][0] if "distances" in results else [0.2] * len(docs)

        for doc, meta, dist in zip(docs, metas, distances):
            # Calculate cosine similarity score (distance is cosine distance)
            similarity = max(0.5, min(0.99, round(1.0 - (dist / 2.0), 2))) if dist is not None else 0.85
            formatted.append({
                "title": meta.get("title", meta.get("filename", "Study Material")),
                "filename": meta.get("filename", "document.txt"),
                "section": meta.get("section", "General Concept"),
                "subject": meta.get("subject", "General"),
                "relevance": similarity,
                "excerpt": doc[:300] + "..." if len(doc) > 300 else doc,
                "full_text": doc
            })
        return formatted

    def add_chunks(self, chunks: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """Index pre-chunked documents into ChromaDB."""
        if not chunks:
            return
        self.collection.upsert(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

    def delete_by_filename(self, filename: str):
        """Remove chunks belonging to a deleted file."""
        try:
            self.collection.delete(where={"filename": filename})
        except Exception as e:
            print(f"Chroma delete error for {filename}: {e}")

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_chunks": self.collection.count(),
            "collection_name": self.collection_name,
            "storage_path": self.chroma_path
        }
