import React, { useState, useEffect, useRef } from 'react';
import { Send, Sparkles, Trash2, PlusCircle, AlertCircle, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import { ChatMessage, HealthStatus } from '../types';
import { ChatBubble } from '../components/ChatBubble';
import { SampleQuestions } from '../components/SampleQuestions';

interface ChatPageProps {
  health: HealthStatus | null;
  conversationId: string | null;
  onNewConversation: () => void;
}

export const ChatPage: React.FC<ChatPageProps> = ({
  health,
  conversationId,
  onNewConversation
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of conversation
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Load existing conversation messages if conversationId changes
  useEffect(() => {
    if (conversationId) {
      loadConversation(conversationId);
    } else {
      setMessages([]);
    }
  }, [conversationId]);

  const loadConversation = async (id: string) => {
    try {
      const data = await api.getConversationDetail(id);
      if (data && data.messages) {
        setMessages(data.messages);
      }
    } catch (err) {
      console.error("Failed to load conversation history", err);
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || inputText).trim();
    if (!query || isLoading) return;

    setErrorMsg(null);
    setInputText('');

    // Add user message to state immediately for snappy UI
    const tempUserMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: query,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMsg]);
    setIsLoading(true);

    try {
      const response = await api.sendMessage(query, conversationId || undefined);

      const botMsg: ChatMessage = {
        id: `bot-${Date.now()}`,
        role: 'assistant',
        content: response.message,
        intent: response.intent,
        topic: response.topic,
        status: response.status,
        tools_used: response.tools_used,
        sources: response.sources,
        activity: response.activity,
        suggested_followups: response.suggested_followups,
        created_at: response.created_at
      };

      setMessages(prev => [...prev, botMsg]);
    } catch (err: any) {
      console.error("Chat error:", err);
      setErrorMsg(
        err.response?.data?.detail ||
        "Unable to communicate with the study assistant backend. Please ensure the server is running on port 8000."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setErrorMsg(null);
  };

  return (
    <div className="flex-1 flex flex-col h-screen bg-slate-950 overflow-hidden">
      {/* Top Header Bar */}
      <header className="h-14 border-b border-slate-800/90 px-6 flex items-center justify-between bg-slate-900/60 backdrop-blur-md shrink-0">
        <div className="flex items-center gap-2">
          <h2 className="text-sm font-bold text-white tracking-wide">
            AI Study Assistant Workspace
          </h2>
          {health?.operational_mode && (
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/30">
              {health.operational_mode}
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onNewConversation}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium transition"
            title="Start fresh conversation"
          >
            <PlusCircle className="w-3.5 h-3.5 text-blue-400" />
            New Session
          </button>
          <button
            onClick={handleClearChat}
            disabled={messages.length === 0}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/60 hover:bg-slate-800 text-slate-400 hover:text-slate-200 text-xs font-medium transition disabled:opacity-40"
            title="Clear current view"
          >
            <Trash2 className="w-3.5 h-3.5" />
            Clear
          </button>
        </div>
      </header>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto px-4 md:px-12 py-6 space-y-4">
        {messages.length === 0 ? (
          <div className="max-w-3xl mx-auto space-y-6 pt-6">
            <div className="text-center space-y-2">
              <div className="inline-flex p-3 rounded-2xl bg-blue-600/20 text-blue-400 mb-2 ring-1 ring-blue-500/30">
                <Sparkles className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold text-white">
                How can I assist your study session today?
              </h3>
              <p className="text-xs text-slate-400 max-w-md mx-auto">
                I am your Agentic AI Study Partner. Ask me to explain difficult computer science concepts, search the study knowledge base, create exam schedules, or quiz your knowledge.
              </p>
            </div>

            {/* Quick Starter Cards */}
            <SampleQuestions onSelect={(q) => handleSendMessage(q)} disabled={isLoading} />
          </div>
        ) : (
          <div className="max-w-4xl mx-auto space-y-4">
            {messages.map((msg) => (
              <ChatBubble
                key={msg.id}
                message={msg}
                onFollowupClick={(followup) => handleSendMessage(followup)}
              />
            ))}

            {/* Loading animation */}
            {isLoading && (
              <div className="flex items-center gap-3 p-4 rounded-xl bg-slate-900 border border-slate-800 max-w-sm text-xs text-slate-300">
                <Loader2 className="w-4 h-4 text-blue-400 animate-spin" />
                <span>Agent analyzing query & searching knowledge base...</span>
              </div>
            )}

            {/* Error banner */}
            {errorMsg && (
              <div className="p-3.5 rounded-xl bg-rose-950/70 border border-rose-800/80 text-rose-200 text-xs flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
                  <span>{errorMsg}</span>
                </div>
                <button
                  onClick={() => handleSendMessage()}
                  className="px-2.5 py-1 bg-rose-800 hover:bg-rose-700 text-white rounded text-xs font-semibold ml-3 shrink-0"
                >
                  Retry
                </button>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Textarea Bar */}
      <div className="p-4 bg-slate-900/80 border-t border-slate-800 shrink-0">
        <div className="max-w-4xl mx-auto">
          <div className="relative flex items-center bg-slate-950 rounded-2xl border border-slate-800 focus-within:border-blue-500 transition shadow-inner">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              rows={1}
              placeholder="Ask a study question (e.g. 'Explain DBMS normalization in simple terms' or 'Quiz me on OS')..."
              className="w-full px-4 py-3.5 bg-transparent text-sm text-slate-100 placeholder-slate-500 focus:outline-none resize-none leading-relaxed"
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={!inputText.trim() || isLoading}
              className="m-2 p-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 active:bg-blue-700 disabled:opacity-30 text-white transition shadow-md shadow-blue-600/30 shrink-0"
              title="Send (Enter)"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          <div className="flex items-center justify-between px-2 pt-2 text-[11px] text-slate-500">
            <span>Press <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono text-[10px]">Enter</kbd> to send, <kbd className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono text-[10px]">Shift + Enter</kbd> for new line</span>
            <span>Agentic AI • RAG • Memory • Tools</span>
          </div>
        </div>
      </div>
    </div>
  );
};
