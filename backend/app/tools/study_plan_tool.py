from typing import Dict, Any, List, Optional

SUBJECT_TOPIC_DEFAULTS = {
    "dbms": [
        "Relational Model & Keys (Candidate, Primary, Foreign)",
        "Database Normalization (1NF, 2NF, 3NF, BCNF)",
        "SQL Queries, Aggregations & Joins",
        "ACID Properties & Transaction Management",
        "Indexing, B+ Trees & Query Optimization",
        "Concurrency Control & 2-Phase Locking",
        "Mock Exam & Full Subject Revision"
    ],
    "operating systems": [
        "Processes, Threads & Process States",
        "CPU Scheduling Algorithms (FCFS, SJF, Round Robin)",
        "Process Synchronization, Mutex & Semaphores",
        "Deadlocks & Banker's Algorithm",
        "Memory Management, Paging & TLB",
        "Virtual Memory & Page Replacement Algorithms",
        "File Systems & Comprehensive Review"
    ],
    "data structures": [
        "Arrays, Strings & Time Complexity Analysis",
        "Singly & Doubly Linked Lists",
        "Stacks, Queues & Monotonic Stacks",
        "Binary Trees & Binary Search Trees (BST)",
        "Graph Traversals (BFS, DFS) & Dijkstra's Algorithm",
        "Sorting Algorithms (Merge Sort, Quick Sort)",
        "Dynamic Programming Basics & Problem Solving"
    ],
    "computer networks": [
        "OSI 7-Layer Model & TCP/IP Architecture",
        "Data Link Layer, MAC & Ethernet Switching",
        "IP Addressing, Subnetting (CIDR) & Routing",
        "Transport Layer: TCP vs UDP & 3-Way Handshake",
        "TCP Flow & Congestion Control Mechanisms",
        "Application Layer: HTTP/HTTPS, DNS & Sockets",
        "Network Security & Final Practice"
    ],
    "java": [
        "Java Syntax, Data Types & JVM Architecture",
        "OOP: Encapsulation, Inheritance & Polymorphism",
        "Java Arrays & String Manipulation",
        "Java Collections Framework (List, Set, Map)",
        "Exception Handling & Custom Exceptions",
        "Multithreading & Synchronization Basics",
        "Practice Coding Problems & Review"
    ],
    "python": [
        "Python Syntax, Lists, Tuples & Dictionaries",
        "Functions, Scope, *args, **kwargs & Recursion",
        "Object-Oriented Programming & Dunder Methods",
        "Generators, Iterators & List Comprehensions",
        "Decorators & Context Managers (with statement)",
        "File I/O & Error Handling",
        "Algorithmic Problem Solving in Python"
    ]
}

class StudyPlanTool:
    name = "Study Plan Generator Tool"
    description = "Generates a personalized, day-by-day study schedule with recommended hours and focused revision modules."

    def execute(
        self,
        subject: str,
        days: int = 5,
        daily_hours: float = 2.5,
        weak_topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        key = subject.lower().strip()
        matched_topics = None
        for k in SUBJECT_TOPIC_DEFAULTS:
            if k in key or key in k:
                matched_topics = SUBJECT_TOPIC_DEFAULTS[k]
                break
        
        if not matched_topics:
            matched_topics = [
                f"Core Fundamentals of {subject}",
                f"Key Principles and Terminology of {subject}",
                f"Intermediate Concepts and Architecture in {subject}",
                f"Practical Exercises and Hands-on Applications of {subject}",
                f"Advanced Scenarios and Problem Solving in {subject}",
                f"Revision and Exam Preparation for {subject}"
            ]

        # Build day-by-day plan
        plan = []
        days_count = max(1, min(14, days))
        
        for day_num in range(1, days_count + 1):
            topic_idx = (day_num - 1) % len(matched_topics)
            topic_focus = matched_topics[topic_idx]
            
            # If weak topics specified, prioritize them
            if weak_topics and day_num <= len(weak_topics):
                topic_focus = f"{topic_focus} (Special Focus: {weak_topics[day_num-1]})"

            if day_num == days_count:
                activities = [
                    f"Comprehensive review of {subject} high-yield topics",
                    "Solve 20 past exam or practice questions",
                    "Formula sheet and definition recap"
                ]
            else:
                activities = [
                    f"Concept Study: Deep dive into {topic_focus} (60 min)",
                    f"Practical Examples & Code/Diagram Trace (45 min)",
                    f"Self-Assessment Quiz & Flashcard review (30 min)"
                ]

            plan.append({
                "day": day_num,
                "focus_topic": topic_focus,
                "duration_hours": daily_hours,
                "activities": activities
            })

        tips = [
            "Active Recall: Test yourself before re-reading notes.",
            "Spaced Repetition: Spend the first 15 minutes of each day reviewing previous day's material.",
            "Use the Quiz Generator tool after each module to verify concept retention.",
            "Hydrate and take a 5-minute break every 30 minutes (Pomodoro technique)."
        ]

        return {
            "subject": subject.upper(),
            "days": days_count,
            "daily_hours": daily_hours,
            "total_study_hours": round(days_count * daily_hours, 1),
            "plan": plan,
            "tips": tips
        }
