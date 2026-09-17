import re
from typing import Tuple, Optional

INTENTS = [
    "Concept Explanation",
    "Question Answering",
    "Exam Preparation",
    "Quiz",
    "Revision",
    "Study Plan",
    "Programming Help",
    "Summarization",
    "Practice Questions",
    "Topic Recommendation",
    "Progress Review",
    "Other"
]

SUBJECTS = [
    "DBMS",
    "Data Structures",
    "Operating Systems",
    "Computer Networks",
    "Java",
    "Python",
    "Web Development",
    "Software Engineering",
    "AI",
    "Machine Learning",
    "Cloud Computing",
    "Computer Organization",
    "Other"
]

SUBJECT_KEYWORDS = {
    "DBMS": ["dbms", "database", "sql", "normalization", "1nf", "2nf", "3nf", "bcnf", "acid", "relational", "primary key", "foreign key", "table", "query", "indexing"],
    "Data Structures": ["dsa", "data structure", "array", "linked list", "stack", "queue", "binary tree", "bst", "graph", "heap", "bfs", "dfs", "sorting", "algorithm"],
    "Operating Systems": ["operating system", "os", "process", "thread", "scheduling", "deadlock", "paging", "virtual memory", "mutex", "semaphore", "banker's", "thrashing", "cpu"],
    "Computer Networks": ["computer network", "networking", "osi", "tcp", "udp", "ip address", "subnet", "dns", "http", "https", "router", "switch", "handshake", "packet"],
    "Java": ["java", "jvm", "jre", "jdk", "arraylist", "inheritance", "polymorphism", "encapsulation", "oop", "collections", "javac"],
    "Python": ["python", "list comprehension", "decorator", "generator", "recursion", "recursive", "def ", "dict", "tuple", "cpython"],
    "Web Development": ["web development", "html", "css", "javascript", "react", "frontend", "backend", "dom", "rest api", "vite", "tailwind"],
    "Software Engineering": ["software engineering", "sdlc", "agile", "scrum", "waterfall", "testing", "solid", "design pattern", "unit test"],
    "AI": ["artificial intelligence", "ai agent", "agentic", "heuristic", "turing test", "a* search", "minimax", "alpha-beta", "knowledge representation"],
    "Machine Learning": ["machine learning", "ml", "supervised", "unsupervised", "regression", "classification", "overfitting", "underfitting", "bias variance", "neural network"],
    "Cloud Computing": ["cloud computing", "cloud", "aws", "azure", "docker", "kubernetes", "iaas", "paas", "saas", "microservices", "virtualization"],
    "Computer Organization": ["computer organization", "architecture", "von neumann", "alu", "registers", "cache", "pipelining", "assembly", "cpu instruction"]
}

def classify_intent_and_subject(message: str, previous_topic: Optional[str] = None) -> Tuple[str, str]:
    text = message.lower()
    
    # 1. Intent Detection
    intent = "Concept Explanation"
    if any(k in text for k in ["quiz", "test me", "mcq", "question paper"]):
        intent = "Quiz"
    elif any(k in text for k in ["study plan", "schedule", "plan for", "prepare in", "days to study", "exam in"]):
        intent = "Study Plan"
    elif any(k in text for k in ["exam preparation", "exam", "syllabus", "prepare for my"]):
        intent = "Exam Preparation"
    elif any(k in text for k in ["summarize", "summary", "brief", "quick notes", "revision notes"]):
        intent = "Summarization"
    elif any(k in text for k in ["practice questions", "practice", "exercises", "problems"]):
        intent = "Practice Questions"
    elif any(k in text for k in ["code", "programming", "function", "syntax", "error", "bug", "implement"]):
        intent = "Programming Help"
    elif any(k in text for k in ["how am i doing", "my progress", "scores", "analytics"]):
        intent = "Progress Review"
    elif any(k in text for k in ["what should i learn", "recommend", "next topic"]):
        intent = "Topic Recommendation"
    elif any(k in text for k in ["revise", "revision"]):
        intent = "Revision"
    elif any(k in text for k in ["explain", "what is", "define", "why does", "difference between", "how does"]):
        intent = "Concept Explanation"
    else:
        intent = "Question Answering"

    # 2. Subject Detection
    subject = "Other"
    best_score = 0
    
    for subj, keywords in SUBJECT_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                score += 2
            elif kw in text:
                score += 1
        if score > best_score:
            best_score = score
            subject = subj

    # If subject was not explicitly in current query, inherit from conversation memory context
    if subject == "Other" and previous_topic and previous_topic != "Other":
        subject = previous_topic

    return intent, subject
