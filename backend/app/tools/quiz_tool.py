from typing import Dict, Any, List, Optional
import random

DEFAULT_QUESTION_BANK = {
    "dbms": [
        {
            "question": "Which normal form deals with the removal of transitive dependencies?",
            "options": ["First Normal Form (1NF)", "Second Normal Form (2NF)", "Third Normal Form (3NF)", "Boyce-Codd Normal Form (BCNF)"],
            "correct_answer": "Third Normal Form (3NF)",
            "explanation": "3NF requires a table to be in 2NF and ensures that no non-prime attribute is transitively dependent on the primary key."
        },
        {
            "question": "What does the 'A' in ACID properties stand for in transaction processing?",
            "options": ["Availability", "Atomicity", "Accuracy", "Authentication"],
            "correct_answer": "Atomicity",
            "explanation": "Atomicity guarantees that all operations within a database transaction complete successfully, or all changes are rolled back ('all or nothing')."
        },
        {
            "question": "Which SQL statement is used to remove all records from a table without logging individual row deletions?",
            "options": ["DELETE", "REMOVE", "TRUNCATE", "DROP"],
            "correct_answer": "TRUNCATE",
            "explanation": "TRUNCATE is a DDL operation that deallocates data pages quickly without logging individual row deletions, unlike DELETE."
        },
        {
            "question": "What type of key refers to the primary key of another table to maintain referential integrity?",
            "options": ["Candidate Key", "Foreign Key", "Super Key", "Alternate Key"],
            "correct_answer": "Foreign Key",
            "explanation": "A Foreign Key in one table references the Primary Key of another table, ensuring referential integrity across relational schemas."
        },
        {
            "question": "Which index physically dictates the ordering of data rows inside the storage file?",
            "options": ["Non-Clustered Index", "Clustered Index", "Secondary Index", "Bitmap Index"],
            "correct_answer": "Clustered Index",
            "explanation": "There can only be one clustered index per table because data rows can only be physically sorted in one order."
        }
    ],
    "operating systems": [
        {
            "question": "Which CPU scheduling algorithm gives the lowest average waiting time for a set of processes?",
            "options": ["First-Come First-Served (FCFS)", "Shortest Job First (SJF)", "Round Robin", "Priority Scheduling"],
            "correct_answer": "Shortest Job First (SJF)",
            "explanation": "SJF is provably optimal for minimizing the average waiting time among non-preemptive scheduling algorithms."
        },
        {
            "question": "Which of the following is NOT one of Coffman's four conditions for deadlock?",
            "options": ["Mutual Exclusion", "Hold and Wait", "Preemption Allowed", "Circular Wait"],
            "correct_answer": "Preemption Allowed",
            "explanation": "The condition is 'No Preemption', meaning resources cannot be forcibly confiscated until voluntarily released."
        },
        {
            "question": "What is the phenomenon called when the system spends more time swapping pages than executing instructions?",
            "options": ["Paging", "Thrashing", "Fragmentation", "Segmentation"],
            "correct_answer": "Thrashing",
            "explanation": "Thrashing occurs when memory is oversubscribed and page replacement algorithms continuously swap pages between RAM and disk."
        },
        {
            "question": "What hardware component translates virtual logical memory addresses into physical RAM addresses?",
            "options": ["ALU", "Translation Lookaside Buffer (TLB)", "Memory Management Unit (MMU)", "Control Unit"],
            "correct_answer": "Memory Management Unit (MMU)",
            "explanation": "The MMU contains the base/limit registers and page table access logic that performs address translation."
        },
        {
            "question": "Which IPC synchronization primitive uses a counter and two atomic functions: wait() and signal()?",
            "options": ["Mutex", "Semaphore", "Spinlock", "Pipe"],
            "correct_answer": "Semaphore",
            "explanation": "A Semaphore is an integer variable used for signaling between concurrent threads or processes using wait() and signal() operations."
        }
    ],
    "data structures": [
        {
            "question": "What is the average time complexity to search for an element in a balanced Binary Search Tree (AVL tree)?",
            "options": ["O(1)", "O(N)", "O(log N)", "O(N log N)"],
            "correct_answer": "O(log N)",
            "explanation": "In a balanced BST, height is bounded by O(log N), allowing search operations to halve the search space at each step."
        },
        {
            "question": "Which data structure is primarily used to implement Breadth-First Search (BFS) in graphs?",
            "options": ["Stack", "Queue", "Priority Queue", "Hash Table"],
            "correct_answer": "Queue",
            "explanation": "BFS explores nodes layer by layer in FIFO order, making a Queue the standard data structure for its frontier."
        },
        {
            "question": "Which sorting algorithm maintains a guaranteed worst-case time complexity of O(N log N)?",
            "options": ["Quick Sort", "Merge Sort", "Bubble Sort", "Insertion Sort"],
            "correct_answer": "Merge Sort",
            "explanation": "Merge Sort always splits arrays in half and performs linear merging, guaranteeing O(N log N) time even in the worst case."
        }
    ],
    "java": [
        {
            "question": "Which Java collection class provides dynamic resizing and fast O(1) random index access?",
            "options": ["LinkedList", "ArrayList", "HashSet", "TreeMap"],
            "correct_answer": "ArrayList",
            "explanation": "ArrayList is implemented using a dynamic backing array, providing O(1) random access by index."
        },
        {
            "question": "What happens if you attempt to access an invalid index of an array in Java?",
            "options": ["Returns null", "Returns 0", "Throws ArrayIndexOutOfBoundsException", "Allocates extra memory"],
            "correct_answer": "Throws ArrayIndexOutOfBoundsException",
            "explanation": "Java performs runtime boundary checks and throws ArrayIndexOutOfBoundsException whenever an out-of-bounds index is accessed."
        }
    ],
    "computer networks": [
        {
            "question": "How many packets are exchanged in a standard TCP connection establishment handshake?",
            "options": ["2 (SYN, ACK)", "3 (SYN, SYN-ACK, ACK)", "4 (SYN, ACK, DATA, FIN)", "1 (CONNECT)"],
            "correct_answer": "3 (SYN, SYN-ACK, ACK)",
            "explanation": "TCP establishes a reliable connection through a 3-way handshake: SYN from client, SYN-ACK from server, and ACK from client."
        },
        {
            "question": "Which protocol is connectionless, lightweight, and ideal for real-time video streaming or online games?",
            "options": ["TCP", "UDP", "FTP", "SMTP"],
            "correct_answer": "UDP",
            "explanation": "UDP eliminates connection handshakes and retransmissions, drastically reducing latency for real-time media."
        }
    ]
}

class QuizGeneratorTool:
    name = "Quiz Generator Tool"
    description = "Generates customized multiple-choice practice quizzes with difficulty ratings and answer explanations."

    def execute(self, subject: str, topic: Optional[str] = None, difficulty: str = "Medium", count: int = 5) -> Dict[str, Any]:
        key = subject.lower().strip()
        matched_pool = None
        for k in DEFAULT_QUESTION_BANK:
            if k in key or key in k:
                matched_pool = DEFAULT_QUESTION_BANK[k]
                break

        if not matched_pool:
            # Universal CS pool fallback
            matched_pool = DEFAULT_QUESTION_BANK["dbms"] + DEFAULT_QUESTION_BANK["operating systems"]

        # Select count
        selected = random.sample(matched_pool, min(count, len(matched_pool)))

        return {
            "subject": subject.upper(),
            "topic": topic or subject,
            "difficulty": difficulty,
            "total_questions": len(selected),
            "questions": selected,
            "instructions": "Select one option per question. Immediate feedback and explanations will be shown."
        }
