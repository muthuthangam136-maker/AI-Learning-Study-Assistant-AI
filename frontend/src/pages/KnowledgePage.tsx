import React, { useState, useEffect } from 'react';
import { BookOpen, Plus, Trash2, Search, FileText, CheckCircle, Database } from 'lucide-react';
import { api } from '../services/api';
import { KnowledgeDocSummary } from '../types';

export const KnowledgePage: React.FC = () => {
  const [docs, setDocs] = useState<KnowledgeDocSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);

  // Form states
  const [newTitle, setNewTitle] = useState('');
  const [newFilename, setNewFilename] = useState('');
  const [newSubject, setNewSubject] = useState('DBMS');
  const [newDescription, setNewDescription] = useState('');
  const [newContent, setNewContent] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadKnowledgeBase();
  }, []);

  const loadKnowledgeBase = async () => {
    try {
      setLoading(true);
      const data = await api.getKnowledgeBase();
      setDocs(data);
    } catch (err) {
      console.error("Failed to load knowledge documents", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string, title: string) => {
    if (!window.confirm(`Are you sure you want to remove '${title}' from the knowledge base?`)) return;
    try {
      await api.deleteKnowledgeDoc(id);
      setDocs(prev => prev.filter(d => d.id !== id));
    } catch (err) {
      alert("Failed to delete document.");
    }
  };

  const handleAddDocument = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newContent.trim()) return;

    try {
      setSubmitting(true);
      const created = await api.addKnowledgeDoc({
        title: newTitle,
        filename: newFilename || `${newTitle.toLowerCase().replace(/\s+/g, '_')}.txt`,
        subject: newSubject,
        description: newDescription,
        content: newContent
      });
      setDocs(prev => [...prev, created]);
      setShowAddModal(false);
      // Reset form
      setNewTitle('');
      setNewFilename('');
      setNewContent('');
      setNewDescription('');
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to add document to knowledge base.");
    } finally {
      setSubmitting(false);
    }
  };

  const filteredDocs = docs.filter(d =>
    d.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.subject.toLowerCase().includes(searchQuery.toLowerCase()) ||
    d.filename.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex-1 flex flex-col h-screen bg-slate-950 overflow-y-auto">
      {/* Header */}
      <header className="border-b border-slate-800/90 px-8 py-6 bg-slate-900/40 shrink-0">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
              <BookOpen className="w-5 h-5 text-blue-400" />
              Study Knowledge Base & RAG Index
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              Curated computer science texts indexed in ChromaDB for high-precision semantic retrieval.
            </p>
          </div>

          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 active:bg-blue-700 text-white text-xs font-semibold shadow-md shadow-blue-600/30 transition self-start md:self-auto"
          >
            <Plus className="w-4 h-4" />
            Add Custom Study Notes
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto w-full p-8 space-y-6">
        {/* Search Bar */}
        <div className="relative max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            placeholder="Search documents by subject, topic or filename..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 transition"
          />
        </div>

        {/* Documents Grid */}
        {loading ? (
          <div className="text-center py-16 text-xs text-slate-400">Loading indexed documents...</div>
        ) : filteredDocs.length === 0 ? (
          <div className="text-center py-16 bg-slate-900/40 border border-slate-800 rounded-2xl p-8">
            <p className="text-sm text-slate-400">No documents found matching your search.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredDocs.map((doc) => (
              <div
                key={doc.id}
                className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-xl p-5 space-y-3 transition shadow-sm flex flex-col justify-between"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 uppercase tracking-wider">
                      {doc.subject}
                    </span>
                    <span className="text-[11px] text-slate-500 font-mono flex items-center gap-1">
                      <Database className="w-3 h-3 text-emerald-400" />
                      {doc.chunks_count} chunks
                    </span>
                  </div>

                  <h3 className="font-bold text-sm text-white">{doc.title}</h3>
                  <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed">
                    {doc.description || "Educational study guide module for computer science."}
                  </p>
                </div>

                <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-500">
                  <span className="font-mono">{doc.filename}</span>
                  <button
                    onClick={() => handleDelete(doc.id, doc.title)}
                    className="p-1 text-slate-500 hover:text-rose-400 transition"
                    title="Delete document"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add Document Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-xl w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-base font-bold text-white">Add Study Material to RAG Knowledge Base</h3>
            <p className="text-xs text-slate-400">
              Your document will be cleaned, divided into semantic chunks, and embedded in ChromaDB.
            </p>

            <form onSubmit={handleAddDocument} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Document Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Distributed Systems & Consensus"
                  value={newTitle}
                  onChange={e => setNewTitle(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Subject</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Distributed Systems"
                    value={newSubject}
                    onChange={e => setNewSubject(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Filename (.txt)</label>
                  <input
                    type="text"
                    placeholder="distributed_systems.txt"
                    value={newFilename}
                    onChange={e => setNewFilename(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Study Content (Markdown / Text)</label>
                <textarea
                  required
                  rows={6}
                  placeholder="Type or paste study text, definitions, concepts and examples..."
                  value={newContent}
                  onChange={e => setNewContent(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-100 focus:outline-none focus:border-blue-500 resize-none font-mono"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 text-xs font-semibold transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold transition disabled:opacity-50"
                >
                  {submitting ? 'Indexing Chunks...' : 'Save & Index in ChromaDB'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
