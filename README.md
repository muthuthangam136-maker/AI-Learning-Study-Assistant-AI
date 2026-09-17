# 🎓 AI LEARNING & STUDY ASSISTANT
### An Agentic AI Full-Stack Educational Platform for IBM / TNSDC Internship

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=flat&logo=fastapi)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-orange?style=flat)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue?style=flat&logo=typescript)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC?style=flat&logo=tailwind-css)
![Status](https://img.shields.io/badge/IBM%2FTNSDC-Internship%20Project-success)

---

## 🌟 1. Project Overview

The **AI Learning & Study Assistant** is an end-to-end, production-ready educational platform engineered with an **Agentic AI** architecture. Designed specifically for college students and self-learners in Computer Science, the assistant doesn't just generate text—it autonomously understands student study intentions, dynamically queries a local **ChromaDB** vector database via **Retrieval-Augmented Generation (RAG)**, executes educational tools (interactive quizzes, personalized study planners, exam notes summarizers), maintains persistent conversation and mastery memory in **SQLite**, and provides step-by-step grounded explanations with teacher-assistance guardrails.

---

## 🚀 2. Key Highlights & Agentic Capabilities

1. **Autonomous Multi-Step Agentic Workflow:**
   - Instead of a simple pass-through to an LLM, the agent performs a 7-stage pipeline:
     $$\text{Request} \rightarrow \text{Intent/Subject Classification} \rightarrow \text{Context Memory} \rightarrow \text{RAG Search} \rightarrow \text{Tool Decision} \rightarrow \text{Tool Execution} \rightarrow \text{Personalized Grounded Answer}$$
2. **Retrieval-Augmented Generation (RAG) with ChromaDB:**
   - 12 comprehensive computer science study guides (DBMS, DSA, OS, Computer Networks, Java, Python, Web Dev, Software Engineering, AI, ML, Cloud, COA) chunked, embedded, and indexed locally.
   - Shows exact source citations, filename, section, relevance match percentage, and preview text.
3. **5 Educational Tools:**
   - 📚 **Study Material Search Tool:** Semantic retrieval across knowledge base chunks.
   - 📝 **Quiz Generator Tool:** Dynamic multiple-choice questions with interactive answers, score calculation, and explanations.
   - 📅 **Study Plan Generator Tool:** Tailored day-by-day revision schedules with hour allocations.
   - 📖 **Topic Summarizer Tool:** High-yield exam revision notes and definitions.
   - 📊 **Difficulty Assessment Tool:** Real-time student mastery estimation.
4. **Relational Conversation & Progress Memory:**
   - Built on SQLite & SQLAlchemy to retain messages, learning goals, quiz performances, and subject breakdown across sessions.
5. **Dual Operation Mode:**
   - **DEMO MODE (Default):** Zero setup or API keys required! Runs immediately offline with rich, pre-configured pedagogical traces and interactive tool executions.
   - **REAL AI MODE:** Seamlessly connects to any OpenAI-compatible API (OpenAI, Ollama, Groq, OpenRouter, vLLM).
6. **Student-Centric Modern Dashboard:**
   - Clean dark-mode interface built with React, Vite, TypeScript, and Tailwind CSS.
   - Features clickable sample prompt pills, interactive quiz widget with live grading, agent execution timeline, and learning progress charts.

---

## 🏛️ 3. System Architecture Diagram

```text
STUDENT (React + Vite + TypeScript Dashboard)
                     │
                     │  HTTP / REST API (Axios)
                     ▼
           FastAPI Backend (Port 8000)
                     │
    ┌────────────────┴────────────────┐
    ▼                                 ▼
[App Lifespan & DB Init]     [Agentic AI Controller]
    │                                 │
    │                   ┌─────────────┴─────────────┐
    │                   ▼                           ▼
    │         1. Intent & Subject          2. Memory Lookup
    │            Classification               (SQLite Context)
    │                   │                           │
    │                   ▼                           ▼
    │         3. RAG Semantic Search       4. Dynamic Tool
    │            (ChromaDB Collection)        Decision Engine
    │                   │                           │
    │                   ▼                           ▼
    │         5. Educational Tool          6. Answer Generator
    │            Execution Engine             (LLM / Demo Engine)
    │                   │                           │
    │                   └─────────────┬─────────────┘
    │                                 │
    ▼                                 ▼
[SQLite Storage]              [Safe Activity Trace]
• Conversations               • Action Milestones
• Messages                    • Grounded Sources
• Study Goals                 • Interactive Quiz Cards
• Quiz Scores                 • Study Roadmaps
```

---

## 🤖 4. Chatbot vs. Agentic AI: The Crucial Difference

For your **IBM / TNSDC Internship evaluation**, here is the core distinction you should highlight to evaluators:

| Feature | Simple Chatbot | AI Learning & Study Assistant (This Project) |
| :--- | :--- | :--- |
| **Execution Flow** | `Prompt -> LLM -> Output` | **7-Stage Autonomous Reasoning Pipeline** |
| **Grounding** | Hallucinates or relies on training cutoff | **RAG over verified ChromaDB vector documents** |
| **Tool Calling** | None (text-only) | **Invokes Quiz, Plan, Summarizer & Assessment Tools** |
| **State & Memory**| Forgets context after window ends | **Persistent SQLite memory for topics, goals & scores** |
| **Safety Guardrails**| Confidently answers even when guessing | **Recommends teacher/instructor consultation when unsure** |
| **Traceability** | Black-box output | **Safe Agent Activity timeline showing step milestones** |

---

## 📁 5. Project Folder Structure

```text
ai-learning-study-assistant/
│
├── frontend/                               # React 18 + Vite + TypeScript Dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx                 # Navigation with mode & ChromaDB status
│   │   │   ├── AgentActivityPanel.tsx      # Safe execution milestones trace
│   │   │   ├── SourcesPanel.tsx            # RAG citation cards with relevance scores
│   │   │   ├── ToolResultCard.tsx          # Interactive Quiz & Study Plan visualizer
│   │   │   ├── SampleQuestions.tsx         # Clickable prompt demonstration pills
│   │   │   └── ChatBubble.tsx              # Markdown, code blocks, follow-up chips
│   │   ├── pages/
│   │   │   ├── ChatPage.tsx                # Main study conversation workspace
│   │   │   ├── KnowledgePage.tsx           # Document library & custom notes adder
│   │   │   ├── ToolsPage.tsx               # 5 educational tools playground
│   │   │   ├── HistoryPage.tsx             # Past study sessions log
│   │   │   ├── ProgressPage.tsx            # Student analytics & quiz stats
│   │   │   └── AboutPage.tsx               # IBM/TNSDC project overview
│   │   ├── services/api.ts                 # Axios REST client
│   │   ├── types/index.ts                  # Type-safe data contracts
│   │   ├── App.tsx                         # App layout & routing
│   │   ├── main.tsx                        # Bootstrap
│   │   └── index.css                       # Modern dark typography & theme
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── backend/                                # FastAPI Python Backend
│   ├── app/
│   │   ├── main.py                         # Server entry & CORS setup
│   │   ├── config.py                       # Pydantic environment settings
│   │   ├── models/
│   │   │   ├── database.py                 # SQLAlchemy relational schema
│   │   │   └── schemas.py                  # Pydantic request/response schemas
│   │   ├── memory/
│   │   │   ├── db.py                       # SQLite connection & table creation
│   │   │   └── memory_service.py           # Context & learning goals service
│   │   ├── rag/
│   │   │   └── vector_store.py             # ChromaDB vector store & embeddings
│   │   ├── tools/
│   │   │   ├── registry.py                 # Tool catalog & registry
│   │   │   ├── study_search_tool.py        # Knowledge retrieval tool
│   │   │   ├── quiz_tool.py                # MCQ quiz generator with answers
│   │   │   ├── study_plan_tool.py          # Day-by-day scheduler
│   │   │   ├── summarizer_tool.py          # Exam revision notes
│   │   │   └── assessment_tool.py          # Mastery assessment
│   │   ├── agents/
│   │   │   ├── classifier.py               # Intent and subject classifier
│   │   │   ├── learning_agent.py           # Core 7-step Agentic workflow
│   │   │   └── demo_data.py                # Pre-configured offline demonstration engine
│   │   └── routes/
│   │       ├── chat.py                     # POST /api/chat & /api/chat/new
│   │       ├── conversations.py            # GET/DELETE /api/conversations
│   │       ├── knowledge.py                # GET/POST/DELETE /api/knowledge
│   │       ├── tools.py                    # GET /api/tools & /api/tools/quiz/submit
│   │       ├── progress.py                 # GET /api/progress
│   │       └── health.py                   # GET /api/health
│   │
│   ├── data/
│   │   └── knowledge_base/                 # 12 Computer Science study texts
│   │       ├── dbms.txt
│   │       ├── data_structures.txt
│   │       ├── operating_systems.txt
│   │       ├── computer_networks.txt
│   │       ├── java.txt
│   │       ├── python.txt
│   │       ├── web_development.txt
│   │       ├── software_engineering.txt
│   │       ├── artificial_intelligence.txt
│   │       ├── machine_learning.txt
│   │       ├── cloud_computing.txt
│   │       └── computer_organization.txt
│   │
│   ├── scripts/
│   │   └── ingest.py                       # Knowledge chunking & ChromaDB indexer
│   ├── requirements.txt
│   └── .env.example
│
├── start-all.bat                           # Master one-click Windows launcher
├── start-backend.bat                       # One-click backend startup script
├── start-frontend.bat                      # One-click frontend startup script
├── docker-compose.yml                      # Optional containerized deployment
├── .gitignore
└── README.md
```

---

## 🛠️ 6. Prerequisites & Installation Guide (Windows)

### Step A: Verify Node.js and Python
Open **Windows PowerShell** or **Command Prompt** and verify your installations:
```powershell
python --version
node --version
npm --version
```
- If Python is not installed, download from [python.org](https://www.python.org/downloads/) (Check **"Add Python to PATH"** during installation).
- If Node.js is not installed, download the LTS release from [nodejs.org](https://nodejs.org/).

---

## ⚡ 7. Quick Start (The Fastest Way on Windows)

Simply double-click:
```text
start-all.bat
```
This launcher will automatically:
1. Initialize the Python virtual environment in `backend/`
2. Install Python dependencies
3. Run the RAG knowledge base ingestion script (`scripts/ingest.py`)
4. Launch the FastAPI server at `http://localhost:8000`
5. Install npm dependencies and launch the Vite frontend at `http://localhost:5173`

---

## 💻 8. Manual Setup Step-by-Step (PowerShell)

If you prefer running step-by-step in separate terminal windows:

### Terminal 1: Backend Setup
```powershell
# 1. Navigate to backend directory
cd ai-learning-study-assistant\backend

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate the virtual environment
.\venv\Scripts\Activate.ps1
# (If PowerShell blocks script execution, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)

# 4. Install backend dependencies
pip install -r requirements.txt

# 5. Create .env configuration file
copy .env.example .env

# 6. Ingest the 12 Knowledge Base documents into ChromaDB
python scripts\ingest.py

# 7. Start the FastAPI backend server
uvicorn app.main:app --reload --port 8000
```
Your backend will be live at:
- **API Root:** `http://localhost:8000`
- **Swagger Documentation:** `http://localhost:8000/docs`

---

### Terminal 2: Frontend Setup
```powershell
# 1. Open a new PowerShell terminal and navigate to frontend
cd ai-learning-study-assistant\frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```
Open your browser at:
👉 **`http://localhost:5173`**

---

## ⚙️ 9. How to Switch Modes

### A. DEMO MODE (Default - Recommended for Offline Presentations)
In `backend/.env`:
```ini
DEMO_MODE=true
```
- Requires **NO API key**.
- Demonstrates complete multi-step reasoning, RAG source citations, and interactive quiz/study plan cards instantly.

### B. REAL AI MODE (OpenAI or Local LLM)
In `backend/.env`:
```ini
DEMO_MODE=false
OPENAI_API_KEY=sk-your-actual-api-key-here
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=
```
- For **Ollama (Free Local LLM)**:
  ```ini
  DEMO_MODE=false
  OPENAI_API_KEY=ollama
  LLM_MODEL=llama3:8b
  LLM_BASE_URL=http://localhost:11434/v1
  ```
- Restart the backend server after changing `.env`.

---

## 🎯 10. Demonstration Scenarios for Internship Review

### Scenario 1: DBMS Normalization (Concept Explanation + RAG)
1. In the chat prompt, click or type:
   > *"Explain DBMS normalization in simple terms."*
2. **Observe the Agent Workflow:**
   - ✓ Request analyzed
   - ✓ Intent classified: **Concept Explanation**
   - ✓ Topic identified: **DBMS**
   - ✓ Knowledge base searched (`dbms.txt`)
   - ✓ Sources retrieved: `dbms.txt` (Database Normalization section, 94% relevance)
   - ✓ Beginner explanation generated with locker analogy and real-world 1NF-BCNF examples.

### Scenario 2: 5-Day Exam Preparation (Tool Selection + Planning)
1. Type:
   > *"I have a DBMS exam in 5 days. Create a study plan."*
2. **Observe the Agent Workflow:**
   - ✓ Intent classified: **Study Plan**
   - ✓ Tool selected: **Study Plan Generator Tool**
   - ✓ Tool executed: 5-day schedule created with 2.5 hours/day
   - ✓ Memory updated: Learning goal recorded in SQLite
   - ✓ Interactive roadmap card displayed in chat.

### Scenario 3: Operating Systems (Interactive Quiz Tool + Progress Tracking)
1. Click or type:
   > *"Quiz me on operating systems."*
2. **Observe the Agent Workflow:**
   - ✓ Intent classified: **Quiz**
   - ✓ Tool selected: **Quiz Generator Tool**
   - ✓ 5 Multiple-Choice Questions generated with options A, B, C, D
   - ✓ Click your answers directly on the interactive card and click **Submit Answers**!
   - ✓ Immediate score calculation, green/red feedback, and explanation displayed.
   - ✓ Navigate to the **Progress** tab in the sidebar to see your score logged in real-time!

---

## 📸 11. Recommended Screenshots for Internship Report

Take screenshots of these screens for your final project documentation:
1. **Home / Study Assistant Screen:** Show the initial welcome screen with clickable prompt pills.
2. **Student Asking a Question:** Show the query input bar.
3. **AI Response with Markdown:** Show formatted definitions, tables, and code snippets.
4. **Agent Activity Panel:** Show the high-level step-by-step milestone timeline.
5. **RAG Grounded Sources Panel:** Expand a source to show `dbms.txt` match and excerpt.
6. **Tool Execution Result (Interactive Quiz):** Show completed quiz with score badge and explanation.
7. **Tool Execution Result (Study Plan):** Show the 5-day roadmap card with hour allocations.
8. **Knowledge Base Page:** Show the grid of 12 indexed CS guides and chunk counts.
9. **Add Custom Knowledge Modal:** Show adding a custom `.txt` study document.
10. **Tools Catalog Page:** Show all 5 educational tools with input/output signatures.
11. **Conversation History Page:** Show multiple saved sessions with delete/resume buttons.
12. **Student Progress Dashboard:** Show real analytics (questions asked, quizzes taken, accuracy rate).
13. **About Project Page:** Show the architecture comparison between simple chatbots and Agentic AI.
14. **Terminal Running Backend:** Show Uvicorn running on port 8000.
15. **FastAPI Swagger UI:** Show `http://localhost:8000/docs` with all endpoints listed.
16. **Terminal Ingestion Output:** Show `python scripts/ingest.py` indexing the 12 documents into ChromaDB.
17. **Engine Mode Pill:** Highlight the "DEMO MODE" or "REAL AI MODE" status badge.

---

## ❓ 12. Troubleshooting Common Issues

- **PowerShell script execution error:**
  Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in PowerShell before activating `venv`.
- **Port 8000 already in use:**
  Run `uvicorn app.main:app --port 8080 --reload` and update `VITE_API_URL` in `frontend/src/services/api.ts`.
- **ChromaDB SQLite version error on older Python:**
  This project uses Python 3.10+ where SQLite 3.35+ is included by default. If on older Windows, upgrade Python.
- **Node module install error:**
  Run `npm cache clean --force` and rerun `npm install`.

---

## 🏆 Project Certification
Built with ❤️ for the **IBM / TNSDC Agentic AI Internship Program**. Demonstrates true autonomous multi-step reasoning, semantic RAG retrieval, tool execution, and stateful memory.

GitHub connection test