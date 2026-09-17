import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { ChatPage } from './pages/ChatPage';
import { KnowledgePage } from './pages/KnowledgePage';
import { ToolsPage } from './pages/ToolsPage';
import { HistoryPage } from './pages/HistoryPage';
import { ProgressPage } from './pages/ProgressPage';
import { AboutPage } from './pages/AboutPage';
import { api } from './services/api';
import { HealthStatus } from './types';

function MainLayout() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [activeConvId, setActiveConvId] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    checkHealth();
    // Poll health periodically
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      const data = await api.getHealth();
      setHealth(data);
    } catch (err) {
      // Fallback health state if backend not immediately reached
      setHealth({
        status: 'connecting',
        project: 'AI Learning & Study Assistant',
        version: '1.0.0',
        demo_mode: true,
        operational_mode: 'DEMO MODE',
        llm_model: 'Built-in Demonstrator',
        chroma_chunks: 12,
        vector_store_active: true,
        agentic_workflow: 'Active'
      });
    }
  };

  const handleNewConversation = async () => {
    try {
      const res = await api.startNewConversation();
      setActiveConvId(res.conversation_id);
    } catch (err) {
      setActiveConvId(`local-${Date.now()}`);
    }
    navigate('/');
  };

  const handleSelectConversation = (id: string) => {
    setActiveConvId(id);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950">
      <Sidebar
        health={health}
        activeConversationId={activeConvId || undefined}
        onNewChat={handleNewConversation}
      />
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        <Routes>
          <Route
            path="/"
            element={
              <ChatPage
                health={health}
                conversationId={activeConvId}
                onNewConversation={handleNewConversation}
              />
            }
          />
          <Route path="/knowledge" element={<KnowledgePage />} />
          <Route path="/tools" element={<ToolsPage />} />
          <Route
            path="/history"
            element={<HistoryPage onSelectConversation={handleSelectConversation} />}
          />
          <Route path="/progress" element={<ProgressPage />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </main>
    </div>
  );
}

export function App() {
  return (
    <Router>
      <MainLayout />
    </Router>
  );
}

export default App;
