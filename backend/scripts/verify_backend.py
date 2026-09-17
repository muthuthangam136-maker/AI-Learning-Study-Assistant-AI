import sys
from pathlib import Path

# Add backend directory to path
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from app.main import app

def test_all():
    print("=" * 60)
    print("[RUNNING AI LEARNING & STUDY ASSISTANT INTEGRATION TESTS]")
    print("=" * 60)
    
    client = TestClient(app)
    
    # 1. Health Endpoint
    print("\n[TEST 1] Testing Health Endpoint (/api/health)...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health_data = res.json()
    print(f"  Status: {health_data['status']}")
    print(f"  Mode:   {health_data['operational_mode']}")
    print(f"  Chunks: {health_data['chroma_chunks']}")
    assert health_data['chroma_chunks'] > 0, "ChromaDB has 0 chunks!"
    print("  -> PASSED [OK]")

    # 2. Knowledge Base Endpoint
    print("\n[TEST 2] Testing Knowledge Base Endpoint (/api/knowledge)...")
    res = client.get("/api/knowledge")
    assert res.status_code == 200
    docs = res.json()
    print(f"  Indexed Documents Count: {len(docs)}")
    assert len(docs) >= 12, f"Expected 12 documents, found {len(docs)}"
    print("  -> PASSED [OK]")

    # 3. Tools Catalog Endpoint
    print("\n[TEST 3] Testing Tools Catalog (/api/tools)...")
    res = client.get("/api/tools")
    assert res.status_code == 200
    tools = res.json()
    print(f"  Registered Tools: {len(tools)}")
    tool_names = [t['name'] for t in tools]
    for t in tool_names:
        print(f"   * {t}")
    assert len(tools) == 5, f"Expected 5 tools, found {len(tools)}"
    print("  -> PASSED [OK]")

    # 4. Chat: DBMS Normalization
    print("\n[TEST 4] Testing Agent RAG & Concept Explanation...")
    chat_payload = {
        "message": "Explain DBMS normalization in simple terms.",
        "subject": "DBMS"
    }
    res = client.post("/api/chat", json=chat_payload)
    assert res.status_code == 200, f"Chat failed: {res.text}"
    chat_data = res.json()
    print(f"  Intent:  {chat_data['intent']}")
    print(f"  Topic:   {chat_data['topic']}")
    print(f"  Sources: {len(chat_data['sources'])}")
    assert chat_data['intent'] == "Concept Explanation"
    assert len(chat_data['sources']) > 0
    print("  -> PASSED [OK]")

    # 5. Chat: 5-Day Study Plan Tool
    print("\n[TEST 5] Testing Agent Tool Selection: Study Plan Generator...")
    chat_payload = {
        "message": "I have a DBMS exam in 5 days. Create a study plan.",
        "conversation_id": chat_data["conversation_id"]
    }
    res = client.post("/api/chat", json=chat_payload)
    assert res.status_code == 200
    plan_data = res.json()
    print(f"  Intent:     {plan_data['intent']}")
    print(f"  Tools Used: {[t['tool_name'] for t in plan_data['tools_used']]}")
    assert any("Study Plan" in t['tool_name'] for t in plan_data['tools_used']), "Study Plan tool was not called!"
    print("  -> PASSED [OK]")

    # 6. Chat: Quiz Generator Tool
    print("\n[TEST 6] Testing Agent Tool Selection: Quiz Generator Tool...")
    chat_payload = {
        "message": "Quiz me on operating systems.",
        "conversation_id": chat_data["conversation_id"]
    }
    res = client.post("/api/chat", json=chat_payload)
    assert res.status_code == 200
    quiz_data = res.json()
    print(f"  Intent:     {quiz_data['intent']}")
    print(f"  Tools Used: {[t['tool_name'] for t in quiz_data['tools_used']]}")
    assert any("Quiz Generator" in t['tool_name'] for t in quiz_data['tools_used']), "Quiz generator tool was not called!"
    print("  -> PASSED [OK]")

    # 7. Progress Analytics
    print("\n[TEST 7] Testing Progress Analytics (/api/progress)...")
    res = client.get("/api/progress")
    assert res.status_code == 200
    prog_data = res.json()
    print(f"  Questions Asked: {prog_data['questions_asked_count']}")
    print(f"  Topics Studied:  {prog_data['topics_studied_count']}")
    print(f"  Sessions:        {prog_data['study_sessions_count']}")
    assert prog_data['questions_asked_count'] >= 3
    print("  -> PASSED [OK]")

    print("\n" + "=" * 60)
    print("[ALL 7 INTEGRATION TESTS PASSED WITH 100% SUCCESS!]")
    print("=" * 60)

if __name__ == "__main__":
    test_all()
