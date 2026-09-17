import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { History, MessageSquare, Trash2, ArrowRight, Calendar, Tag } from 'lucide-react';
import { api } from '../services/api';
import { ConversationSummary } from '../types';

interface HistoryPageProps {
  onSelectConversation: (id: string) => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ onSelectConversation }) => {
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await api.getConversations();
      setConversations(data);
    } catch (err) {
      console.error("Failed to load conversation history", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!window.confirm("Are you sure you want to delete this study session?")) return;
    try {
      await api.deleteConversation(id);
      setConversations(prev => prev.filter(c => c.id !== id));
    } catch (err) {
      alert("Failed to delete conversation.");
    }
  };

  const handleOpen = (id: string) => {
    onSelectConversation(id);
    navigate('/');
  };

  return (
    <div className="flex-1 flex flex-col h-screen bg-slate-950 overflow-y-auto">
      {/* Header */}
      <header className="border-b border-slate-800/90 px-8 py-6 bg-slate-900/40 shrink-0">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
            <History className="w-5 h-5 text-blue-400" />
            Study Session History & Memory Log
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Persisted learning sessions stored in SQLite conversation memory. Resume any previous dialogue.
          </p>
        </div>
      </header>

      {/* List Area */}
      <div className="max-w-4xl mx-auto w-full p-8">
        {loading ? (
          <div className="text-center py-16 text-xs text-slate-400">Loading study history...</div>
        ) : conversations.length === 0 ? (
          <div className="text-center py-16 bg-slate-900/40 border border-slate-800 rounded-2xl p-8 space-y-3">
            <MessageSquare className="w-8 h-8 text-slate-500 mx-auto" />
            <h3 className="text-sm font-semibold text-slate-300">No learning conversations yet</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Start your first study session in the Study Assistant tab to record your learning questions.
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {conversations.map((conv) => (
              <div
                key={conv.id}
                onClick={() => handleOpen(conv.id)}
                className="bg-slate-900 border border-slate-800 hover:border-blue-500/50 rounded-xl p-4 transition cursor-pointer flex items-center justify-between group shadow-sm"
              >
                <div className="space-y-1.5 flex-1 pr-4">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-white group-hover:text-blue-400 transition">
                      {conv.title}
                    </span>
                    {conv.subject && conv.subject !== 'General' && (
                      <span className="text-[10px] px-2 py-0.2 rounded-full bg-blue-500/10 text-blue-300 border border-blue-500/20 font-medium">
                        {conv.subject}
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-4 text-[11px] text-slate-400">
                    <span className="flex items-center gap-1">
                      <MessageSquare className="w-3 h-3 text-slate-500" />
                      {conv.message_count} messages
                    </span>
                    <span className="flex items-center gap-1 font-mono text-[10px] text-slate-500">
                      <Calendar className="w-3 h-3" />
                      {new Date(conv.updated_at).toLocaleString()}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    onClick={(e) => handleDelete(e, conv.id)}
                    className="p-2 text-slate-500 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition"
                    title="Delete session"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                  <span className="p-2 text-slate-500 group-hover:text-blue-400 transition">
                    <ArrowRight className="w-4 h-4" />
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
