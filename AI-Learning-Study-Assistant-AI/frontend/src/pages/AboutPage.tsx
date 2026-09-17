import React from 'react';
import { Info, CheckCircle2, Layers, Cpu, Database, Wrench, ShieldCheck, Award } from 'lucide-react';

export const AboutPage: React.FC = () => {
  const concepts = [
    { title: "Autonomous Decision Making", desc: "The agent analyzes the student's request, classifies the intent and topic, and determines the optimal execution path without manual user scripting." },
    { title: "Tool Selection & Execution", desc: "Selects and calls specialized educational tools (Quiz Generator, Study Plan Generator, Summarizer, Assessment) when needed." },
    { title: "Retrieval-Augmented Generation (RAG)", desc: "Searches localized ChromaDB embeddings of 12 comprehensive computer science guides to ground all answers with verified citations." },
    { title: "Conversation & Learning Memory", desc: "Maintains short-term chat context and long-term learning goals and quiz accuracy inside a persistent SQLite relational store." },
    { title: "Multi-Step Workflow", desc: "Follows a structured 7-stage pipeline: Intent Analysis -> Topic Tagging -> Context Lookup -> RAG Retrieval -> Tool Decision -> Execution -> Personalized Delivery." },
    { title: "Personalized Pedagogy", desc: "Adapts technical depth based on conversational context, beginner vs advanced query framing, and prior quiz performance." },
    { title: "Teacher Guidance Fallback", desc: "Transparently identifies when knowledge confidence is low and explicitly directs the student to instructor assistance." },
    { title: "Execution Trace (Safe Activity)", desc: "Exposes high-level action milestones in the UI without revealing raw internal chain-of-thought, ensuring professional presentation." }
  ];

  const techStack = [
    { name: "React + Vite + TypeScript", category: "Frontend Framework", desc: "Modern, high-performance responsive student dashboard with type safety." },
    { name: "Tailwind CSS", category: "Styling & UI", desc: "Tailored educational dark theme with glassmorphism and subtle animations." },
    { name: "FastAPI + Uvicorn", category: "Backend REST API", desc: "High-throughput asynchronous Python web framework with auto-generated OpenAPI docs." },
    { name: "ChromaDB", category: "Vector Database", desc: "Local embedded vector store for cosine similarity indexing and retrieval." },
    { name: "Sentence-Transformers", category: "Embedding Model", desc: "Local semantic text embeddings running offline without paid embedding APIs." },
    { name: "OpenAI-Compatible LLM Architecture", category: "AI Reasoning", desc: "Flexible integration supporting OpenAI, Ollama, Groq, or OpenRouter with full offline Demo Mode." },
    { name: "SQLite + SQLAlchemy", category: "Database & Memory", desc: "Relational persistence for conversations, messages, study goals, and quiz scores." }
  ];

  return (
    <div className="flex-1 flex flex-col h-screen bg-slate-950 overflow-y-auto">
      {/* Header */}
      <header className="border-b border-slate-800/90 px-8 py-6 bg-slate-900/40 shrink-0">
        <div className="max-w-5xl mx-auto">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase tracking-widest">
              IBM / TNSDC Internship Project
            </span>
          </div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
            <Info className="w-5 h-5 text-blue-400" />
            AI Learning & Study Assistant
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            An Agentic AI system that understands learning needs, searches study materials via RAG, uses educational tools, remembers conversations, and explains concepts step-by-step.
          </p>
        </div>
      </header>

      {/* Main Body */}
      <div className="max-w-5xl mx-auto w-full p-8 space-y-10">
        {/* Simple Chatbot vs Agentic AI Callout */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-sm">
          <h3 className="font-bold text-base text-white flex items-center gap-2">
            <Cpu className="w-5 h-5 text-indigo-400" />
            Why This is an Agentic AI System (Not a Simple Chatbot)
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs pt-2">
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-2">
              <span className="text-rose-400 font-bold uppercase tracking-wider text-[10px]">
                ❌ Traditional Simple Chatbot
              </span>
              <p className="text-slate-300">
                Single-pass generation: <code className="text-slate-400">User Query $\rightarrow$ LLM Prompt $\rightarrow$ Generic Answer</code>
              </p>
              <ul className="text-slate-400 space-y-1 list-disc list-inside text-[11px]">
                <li>No dynamic tool invocation</li>
                <li>Hallucinates facts without grounded document retrieval</li>
                <li>Forgets learning goals between questions</li>
                <li>Cannot adapt execution workflow dynamically</li>
              </ul>
            </div>

            <div className="p-4 rounded-xl bg-blue-950/30 border border-blue-800/50 space-y-2">
              <span className="text-emerald-400 font-bold uppercase tracking-wider text-[10px]">
                ✅ AI Learning & Study Assistant (This Project)
              </span>
              <p className="text-slate-200">
                Autonomous Multi-Step Agentic Reasoning:
              </p>
              <ul className="text-slate-300 space-y-1 list-disc list-inside text-[11px]">
                <li><strong className="text-blue-300">Intent & Topic Classification:</strong> Dissects educational objective</li>
                <li><strong className="text-blue-300">Semantic RAG Retrieval:</strong> Searches ChromaDB with citations</li>
                <li><strong className="text-blue-300">Tool Selection & Execution:</strong> Generates quizzes and study plans</li>
                <li><strong className="text-blue-300">Relational Memory:</strong> Tracks topics and quiz scores in SQLite</li>
                <li><strong className="text-blue-300">Pedagogical Guardrails:</strong> Recommends teacher consultation when unsure</li>
              </ul>
            </div>
          </div>
        </div>

        {/* 8 Core Agentic AI Concepts */}
        <div className="space-y-4">
          <h3 className="font-bold text-base text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-400" />
            Core Agentic AI Concepts Demonstrated
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {concepts.map((c, i) => (
              <div key={i} className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-1.5">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <h4 className="font-semibold text-xs text-white">{c.title}</h4>
                </div>
                <p className="text-[11px] text-slate-400 pl-6 leading-relaxed">{c.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Technology Stack Table */}
        <div className="space-y-4">
          <h3 className="font-bold text-base text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-blue-400" />
            Full-Stack Technology Architecture
          </h3>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden text-xs">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-950 border-b border-slate-800 text-slate-400 text-[11px]">
                  <th className="p-3.5 font-semibold">Technology</th>
                  <th className="p-3.5 font-semibold">Role</th>
                  <th className="p-3.5 font-semibold">Description</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {techStack.map((tech, idx) => (
                  <tr key={idx} className="hover:bg-slate-850/50">
                    <td className="p-3.5 font-semibold text-white">{tech.name}</td>
                    <td className="p-3.5 text-blue-300">{tech.category}</td>
                    <td className="p-3.5 text-slate-400 leading-relaxed">{tech.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Internship Evaluation Footer */}
        <div className="p-5 bg-gradient-to-r from-blue-950/40 to-indigo-950/40 border border-blue-800/40 rounded-2xl flex items-center justify-between text-xs">
          <div className="space-y-1">
            <h4 className="font-bold text-white">Project Evaluation Ready</h4>
            <p className="text-[11px] text-slate-400">
              Complete with Swagger Docs, ChromaDB Vector Pipeline, Windows Automation Scripts, and Offline Demo Mode.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 bg-blue-600 text-white font-bold rounded-lg text-xs">
              Version 1.0.0
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
