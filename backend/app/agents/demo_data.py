from typing import Dict, Any, List

def get_demo_response(message: str, intent: str, subject: str) -> Dict[str, Any]:
    text = message.lower()
    
    # 1. DBMS Normalization
    if "normalization" in text or ("dbms" in text and "explain" in text):
        return {
            "intent": "Concept Explanation",
            "topic": "DBMS",
            "status": "answered",
            "tools_used": [],
            "sources": [
                {
                    "title": "Database Management Systems Guide",
                    "filename": "dbms.txt",
                    "section": "Database Normalization (Step-by-Step)",
                    "relevance": 0.94,
                    "excerpt": "Normalization is the process of organizing data in a database to reduce data redundancy, eliminate data anomalies..."
                }
            ],
            "message": """### 📘 Topic: DBMS Normalization

#### 🌟 Simple Explanation
Imagine organizing a messy school locker. If you keep textbooks, gym clothes, and snacks thrown together in every compartment, you waste time and cause confusion. **Database Normalization** is like organizing that locker by systematically dividing large, messy tables into smaller, well-structured tables without losing data relationships.

#### 🎯 Why It Is Needed
Without normalization, databases suffer from **Data Anomalies**:
1. **Insertion Anomaly:** You cannot add a new record without inserting unnecessary dummy data.
2. **Deletion Anomaly:** Deleting one detail (e.g., student dropped a course) inadvertently deletes other critical data (e.g., course info).
3. **Update Anomaly:** If one piece of duplicate data changes, you must update it in multiple rows; missing one causes data inconsistency.

---

#### 🪜 Step-by-Step Normal Forms

1. **First Normal Form (1NF): Atomicity**
   - Every column must contain single, indivisible (atomic) values.
   - *Example:* Instead of `Courses: "DBMS, Java"`, create separate rows for each course.

2. **Second Normal Form (2NF): No Partial Dependency**
   - Must already be in 1NF.
   - All non-key columns must depend on the **entire** composite primary key, not just a portion of it.

3. **Third Normal Form (3NF): No Transitive Dependency**
   - Must already be in 2NF.
   - Non-key columns cannot depend on other non-key columns ($A \\rightarrow B \\rightarrow C$).
   - Rule: For every $X \\rightarrow Y$, $X$ must be a Super Key or $Y$ is a Prime Attribute.

4. **Boyce-Codd Normal Form (BCNF)**
   - Stricter 3NF where for every functional dependency $X \\rightarrow Y$, $X$ must strictly be a Super Key.

---

#### 💡 Real-World Example
Suppose we have an unnormalized table:
`Students(StudentID, StudentName, DeptID, DeptHead)`

- If `StudentID -> DeptID` and `DeptID -> DeptHead`, then `DeptHead` transitively depends on `StudentID`.
- **To normalize to 3NF:** Split into two clean tables:
  1. `Students(StudentID, StudentName, DeptID)`
  2. `Departments(DeptID, DeptHead)`

#### 📌 Key Takeaways
- Higher normal forms decrease redundancy but require more SQL `JOIN` operations.
- Most commercial applications normalize up to **3NF / BCNF**.

Would you like to solve a quick practice question on identifying 2NF vs 3NF?""",
            "suggested_followups": [
                "Give me a practice question on 2NF vs 3NF",
                "What is Boyce-Codd Normal Form (BCNF)?",
                "Create a 5-day study plan for DBMS"
            ]
        }

    # 2. 5-Day Study Plan for DBMS or Exam Prep
    elif "study plan" in text or "plan" in text or ("exam" in text and "5 days" in text):
        from app.tools.study_plan_tool import StudyPlanTool
        tool = StudyPlanTool()
        plan_result = tool.execute(subject=subject if subject != "Other" else "DBMS", days=5, daily_hours=2.5, weak_topics=["SQL Queries & Joins", "Normalization 2NF/3NF"])
        
        return {
            "intent": "Study Plan",
            "topic": subject if subject != "Other" else "DBMS",
            "status": "answered",
            "tools_used": [
                {
                    "tool_name": "Study Plan Generator Tool",
                    "action": "Generated personalized 5-day exam preparation schedule",
                    "result": plan_result
                }
            ],
            "sources": [
                {
                    "title": "Database Management Systems Guide",
                    "filename": "dbms.txt",
                    "section": "SQL Fundamentals & Joins",
                    "relevance": 0.91,
                    "excerpt": "Joins, ACID properties, transaction schedules and normalization..."
                }
            ],
            "message": f"""### 📅 5-Day Personalized Study Plan: {subject if subject != "Other" else "DBMS"}

I have analyzed your exam preparation timeline (5 days remaining, allocating **2.5 hours/day** for a total of **12.5 study hours**). Extra focus has been scheduled for SQL and Normalization.

---

#### 🗓️ Day-by-Day Schedule

- **Day 1: Relational Model, Keys & ER Diagrams** (2.5 hrs)
  - Understand Candidate Keys, Primary Keys, and Foreign Key constraints.
  - Review ER diagram notations and cardinality mappings.
  - *Checkpoint:* Complete 5 key identification practice exercises.

- **Day 2: Database Normalization (Deep Dive)** (2.5 hrs)
  - Master 1NF, 2NF (eliminating partial dependency), and 3NF/BCNF (transitive dependency).
  - Practice functional dependency decompositions.
  - *Checkpoint:* Classify 3 sample schemas into their respective normal forms.

- **Day 3: SQL Mastery & Complex Joins** (2.5 hrs)
  - Hands-on SQL: `INNER JOIN`, `LEFT OUTER JOIN`, `GROUP BY`, and `HAVING`.
  - Subqueries, views, and aggregate functions.
  - *Checkpoint:* Write 10 SQL queries covering real-world join conditions.

- **Day 4: Transactions, ACID Properties & Concurrency Control** (2.5 hrs)
  - Detailed breakdown of Atomicity, Consistency, Isolation, Durability.
  - Serializability, 2-Phase Locking (2PL), and Deadlock handling.
  - *Checkpoint:* Trace a concurrent schedule and check for conflict serializability.

- **Day 5: Indexing, B+ Trees & Comprehensive Mock Exam** (2.5 hrs)
  - Clustered vs Non-Clustered Indexes and performance implications.
  - Full-length 20-question practice test under timed conditions.
  - Rapid flashcard review of definitions and formulas.

---

💡 **Pro Study Tip:** Spend the first 15 minutes of every day recalling the previous day's concepts without looking at your notes (Active Recall).

Would you like me to start a diagnostic quiz to test your baseline right now?""",
            "suggested_followups": [
                "Quiz me on DBMS normalization",
                "Explain ACID properties with an example",
                "What is the difference between Clustered and Non-Clustered Index?"
            ]
        }

    # 3. Quiz on Operating Systems
    elif "quiz" in text or "test me" in text:
        from app.tools.quiz_tool import QuizGeneratorTool
        quiz_tool = QuizGeneratorTool()
        target_subject = subject if subject != "Other" else "Operating Systems"
        quiz_result = quiz_tool.execute(subject=target_subject, count=5)
        
        return {
            "intent": "Quiz",
            "topic": target_subject,
            "status": "answered",
            "tools_used": [
                {
                    "tool_name": "Quiz Generator Tool",
                    "action": f"Generated 5 multiple-choice questions for {target_subject}",
                    "result": quiz_result
                }
            ],
            "sources": [
                {
                    "title": "Operating Systems Concepts Guide",
                    "filename": "operating_systems.txt",
                    "section": "Process Synchronization & CPU Scheduling",
                    "relevance": 0.95,
                    "excerpt": "CPU scheduling algorithms, semaphore operations, deadlock conditions..."
                }
            ],
            "message": f"""### 📝 Practice Quiz: {target_subject}

I have prepared an interactive **5-question multiple choice quiz** to test your understanding of core concepts in **{target_subject}**.

Take a look at the interactive Quiz Card in the workspace or answer the questions below:

1. **Which CPU scheduling algorithm provides the lowest average waiting time for a set of processes?**
   - A) First-Come First-Served (FCFS)
   - B) Shortest Job First (SJF)
   - C) Round Robin
   - D) Priority Scheduling
   *(Correct: **B** - SJF is provably optimal for minimizing average waiting time).*

2. **Which of the following is NOT one of Coffman's four conditions for deadlock?**
   - A) Mutual Exclusion
   - B) Hold and Wait
   - C) Preemption Allowed
   - D) Circular Wait
   *(Correct: **C** - The condition is 'No Preemption').*

3. **What is the phenomenon called when the system spends more time swapping pages than executing instructions?**
   - A) Thrashing
   - B) Paging
   - C) Fragmentation
   - D) Segmentation
   *(Correct: **A** - Thrashing occurs when RAM is overcommitted).*

Submit your answers or use the interactive quiz tool in the dashboard to record your score in your student progress tracker!""",
            "suggested_followups": [
                "Explain the difference between Mutex and Semaphore",
                "Explain Banker's Algorithm for deadlock avoidance",
                "Show my learning progress"
            ]
        }

    # 4. TCP vs UDP
    elif "tcp" in text or "udp" in text:
        return {
            "intent": "Concept Explanation",
            "topic": "Computer Networks",
            "status": "answered",
            "tools_used": [],
            "sources": [
                {
                    "title": "Computer Networks & Protocols",
                    "filename": "computer_networks.txt",
                    "section": "Transport Layer: TCP vs. UDP",
                    "relevance": 0.96,
                    "excerpt": "TCP is connection-oriented with 3-way handshake; UDP is connectionless and low-latency..."
                }
            ],
            "message": """### 🌐 Comparison: TCP vs. UDP (Transport Layer Protocols)

Both TCP and UDP operate at Layer 4 (Transport Layer) of the OSI model, but they make opposite trade-offs between **reliability** and **speed**.

| Feature | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
| :--- | :--- | :--- |
| **Connection Type** | Connection-Oriented (Requires 3-Way Handshake) | Connectionless (Sends immediately) |
| **Reliability** | Guaranteed delivery (Retransmits lost packets) | Best-effort (Lost packets are discarded) |
| **Data Ordering** | Guarantees packets arrive in exact order | Packets may arrive out of order |
| **Header Overhead** | 20 to 60 bytes | Lightweight: strictly 8 bytes |
| **Flow & Congestion Control** | Yes (Sliding window & AIMD) | No congestion control |
| **Speed / Latency** | Higher latency due to acknowledgments | Ultra-low latency |
| **Real-World Use Cases** | Web pages (HTTP/HTTPS), File transfers, Email | Video streaming, Live broadcasts, Online multiplayer gaming, DNS queries |

---

#### 🤝 The TCP 3-Way Handshake:
1. **SYN:** Client sends Synchronize sequence number to Server.
2. **SYN-ACK:** Server acknowledges and sends its own Synchronize packet.
3. **ACK:** Client acknowledges server, connection is established!

Would you like to examine how DNS uses UDP for fast queries?""",
            "suggested_followups": [
                "How does the TCP 3-Way Handshake work?",
                "Why does DNS prefer UDP over TCP?",
                "Create a study plan for Computer Networks"
            ]
        }

    # 5. Java Arrays & Practice Questions
    elif "java" in text and ("array" in text or "practice" in text):
        return {
            "intent": "Practice Questions",
            "topic": "Java",
            "status": "answered",
            "tools_used": [],
            "sources": [
                {
                    "title": "Java Programming & OOP",
                    "filename": "java.txt",
                    "section": "Java Arrays and Memory Representation",
                    "relevance": 0.93,
                    "excerpt": "An array in Java is an object that stores elements of the same type at contiguous memory locations..."
                }
            ],
            "message": """### ☕ Java Arrays: Concept & 10 Practice Questions

In Java, an array is a dynamically created object that holds a fixed number of values of a single type in contiguous heap memory.
Index begins at `0` and ends at `length - 1`. Accessing an out-of-bounds index throws `ArrayIndexOutOfBoundsException`.

---

#### 📋 10 High-Yield Practice Questions for Java Arrays:

1. **Array Reversal:** Write a method to reverse an integer array in-place with $O(1)$ auxiliary memory.
2. **Find Missing Number:** Given an array containing $N-1$ distinct integers from $1$ to $N$, find the missing integer in $O(N)$ time.
3. **Two Sum Problem:** Given an array of integers and a target sum, return indices of the two numbers that add up to the target.
4. **Remove Duplicates:** Remove duplicates in-place from a sorted array and return the new length.
5. **Rotate Array:** Rotate an array to the right by $K$ steps.
6. **Maximum Subarray (Kadane's Algorithm):** Find the contiguous subarray with the largest sum.
7. **Merge Sorted Arrays:** Merge two sorted integer arrays into one sorted array without extra space.
8. **Segregate 0s and 1s:** Traverse an array of 0s and 1s and sort them in a single pass ($O(N)$).
9. **Find Peak Element:** Find an element that is strictly greater than its neighbors using Binary Search in $O(\\log N)$.
10. **Intersection of Two Arrays:** Compute the common elements between two integer arrays using a `HashSet`.

Which problem would you like to solve first? I can provide code hints or explain the step-by-step optimal algorithm!""",
            "suggested_followups": [
                "Show me the code solution for Kadane's Algorithm",
                "Explain the Two Sum problem with HashMap",
                "Quiz me on Java OOP concepts"
            ]
        }

    # 6. Recursion Explanation
    elif "recursion" in text or "recursive" in text:
        return {
            "intent": "Concept Explanation",
            "topic": "Python",
            "status": "answered",
            "tools_used": [],
            "sources": [
                {
                    "title": "Python Language & Techniques",
                    "filename": "python.txt",
                    "section": "Functions, Recursion and Scope",
                    "relevance": 0.92,
                    "excerpt": "Recursion: A function that solves a problem by calling itself with smaller subproblems..."
                }
            ],
            "message": """### 🔁 Understanding Recursion (Step-by-Step)

#### 🌟 Simple Analogy: Russian Matryoshka Dolls
Think of opening a large nesting wooden doll. Inside is a slightly smaller doll. You continue opening dolls until you find the tiniest, solid doll that cannot be opened. That tiny doll is your **Base Case**. Once reached, you put each doll back together in reverse order.

---

#### 🧱 The Two Fundamental Rules of Recursion:
1. **The Base Case:** The condition where the function stops calling itself and returns a direct value. Without this, you get a `RecursionError` / Stack Overflow.
2. **The Recursive Step:** The function calls itself with a smaller piece of the problem, progressing closer to the base case.

---

#### 💻 Step-by-Step Code Walkthrough (Factorial in Python)
```python
def factorial(n: int) -> int:
    # 1. Base Case: When n is 1 or 0, return 1 immediately
    if n <= 1:
        return 1
    
    # 2. Recursive Case: Multiply n by the result of factorial(n - 1)
    return n * factorial(n - 1)

print(factorial(4)) # Output: 24
```

#### 📦 What Happens on the Call Stack:
```
[Push] factorial(4) = 4 * factorial(3)
  [Push] factorial(3) = 3 * factorial(2)
    [Push] factorial(2) = 2 * factorial(1)
      [Push] factorial(1) returns 1 (BASE CASE REACHED!)
    [Pop] factorial(2) computes 2 * 1 = 2
  [Pop] factorial(3) computes 3 * 2 = 6
[Pop] factorial(4) computes 4 * 6 = 24
```

Would you like to write a recursive function together for reversing a string or generating Fibonacci numbers?""",
            "suggested_followups": [
                "Explain the Call Stack in recursion",
                "Show me Fibonacci with recursion and memoization",
                "Give me 5 beginner recursion practice problems"
            ]
        }

    # 7. Summarize OS Process Management
    elif "summarize" in text or "process management" in text:
        from app.tools.summarizer_tool import TopicSummarizerTool
        tool = TopicSummarizerTool()
        summary_result = tool.execute(topic="OS Process Management")
        
        return {
            "intent": "Summarization",
            "topic": "Operating Systems",
            "status": "answered",
            "tools_used": [
                {
                    "tool_name": "Topic Summarizer Tool",
                    "action": "Generated executive revision summary for OS Process Management",
                    "result": summary_result
                }
            ],
            "sources": [
                {
                    "title": "Operating Systems Concepts Guide",
                    "filename": "operating_systems.txt",
                    "section": "Processes, Threads, and CPU Scheduling",
                    "relevance": 0.97,
                    "excerpt": "Process vs Thread, Process states, scheduling algorithms FCFS, SJF, RR..."
                }
            ],
            "message": """### 📖 Executive Summary: OS Process Management

#### 1. Process vs. Thread
- **Process:** An executing program instance with independent address space (Text, Data, Heap, Stack) and a Process Control Block (PCB). Heavyweight context switching.
- **Thread:** Lightweight execution unit within a process. Threads share address space and file descriptors, but maintain private program counters and call stacks.

#### 2. Process Lifecycle States
`New` $\\rightarrow$ `Ready` (waiting for CPU) $\\rightarrow$ `Running` $\\rightarrow$ `Waiting/Blocked` (I/O) $\\rightarrow$ `Terminated`.

#### 3. CPU Scheduling Cheat Sheet
- **FCFS:** Simple, non-preemptive; suffers from Convoy Effect.
- **SJF:** Provably optimal average waiting time; risks starvation for long processes.
- **Round Robin:** Preemptive time-sliced; ideal for interactive time-sharing systems.

#### 4. High-Yield Exam Checklist
- Explain difference between Preemptive and Non-Preemptive scheduling.
- List all 4 Coffman conditions for Deadlock.
- Contrast Mutex (binary ownership) vs Semaphore (counting resource signaling).""",
            "suggested_followups": [
                "Quiz me on Operating Systems",
                "Explain Round Robin scheduling with Gantt chart",
                "What is the difference between Mutex and Semaphore?"
            ]
        }

    # 8. General AI / Computer Science Query
    else:
        return {
            "intent": intent,
            "topic": subject if subject != "Other" else "General CS",
            "status": "answered",
            "tools_used": [],
            "sources": [
                {
                    "title": f"{subject} Study Material" if subject != "Other" else "Computer Science Guide",
                    "filename": f"{subject.lower().replace(' ', '_')}.txt" if subject != "Other" else "data_structures.txt",
                    "section": "Core Concepts",
                    "relevance": 0.88,
                    "excerpt": "Fundamental principles, definitions and architectural trade-offs..."
                }
            ],
            "message": f"""### 🎓 Study Assistance: {subject if subject != "Other" else "Computer Science"}

Here is an analysis of your learning question:

#### 📌 Overview
You asked: *"{message}"*. This falls under **{subject}** with the primary objective classified as **{intent}**.

#### 💡 Key Concepts
- When mastering this topic, prioritize understanding the foundational definitions and architectural constraints before diving into optimization.
- Break the problem down into inputs, transformations, and expected outputs.
- Verify boundary conditions (empty inputs, maximum limits, edge values).

#### 🎯 Recommended Action
Feel free to ask for:
1. A **step-by-step explanation** with analogies
2. A **practical code example** with output
3. An interactive **quiz** to test your retention
4. A **customized study plan** if you are preparing for an upcoming exam!""",
            "suggested_followups": [
                f"Quiz me on {subject if subject != 'Other' else 'DBMS'}",
                f"Create a 5-day study plan for {subject if subject != 'Other' else 'DBMS'}",
                "Give me 5 practice questions"
            ]
        }
