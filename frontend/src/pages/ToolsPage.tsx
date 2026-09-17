import React, { useState, useEffect } from 'react';
import { Wrench, BookCheck, Calendar, BookOpen, FileText, BarChart3, CheckCircle2, Play } from 'lucide-react';
import { api } from '../services/api';
import { ToolDefinition } from '../types';
import { ToolResultCard } from '../components/ToolResultCard';

export const ToolsPage: React.FC = () => {
  const [tools, setTools] = useState<ToolDefinition[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTestTool, setActiveTestTool] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<any>(null);

  useEffect(() => {
    loadTools();
  }, []);

  const loadTools = async () => {
    try {
      setLoading(true);
      const data = await api.getTools();
      setTools(data);
    } catch (err) {
      console.error("Failed to load tools", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunSampleQuiz = () => {
    setActiveTestTool('quiz_generator');
    setTestResult({
      tool_name: 'Quiz Generator Tool',
      action: 'Generated 5 sample questions for Operating Systems',
      result: {
        subject: 'OPERATING SYSTEMS',
        topic: 'Operating Systems',
        difficulty: 'Medium',
        questions: [
          {
            question: "Which CPU scheduling algorithm gives the lowest average waiting time for a set of processes?",
            options: ["First-Come First-Served (FCFS)", "Shortest Job First (SJF)", "Round Robin", "Priority Scheduling"],
            correct_answer: "Shortest Job First (SJF)",
            explanation: "SJF is provably optimal for minimizing average waiting time among non-preemptive algorithms."
          },
          {
            question: "What is the phenomenon called when the system spends more time swapping pages than executing instructions?",
            options: ["Paging", "Thrashing", "Fragmentation", "Segmentation"],
            correct_answer: "Thrashing",
            explanation: "Thrashing occurs when memory is oversubscribed and pages are continually swapped between RAM and disk."
          }
        ]
      }
    });
  };

  const handleRunSamplePlan = () => {
    setActiveTestTool('study_plan');
    setTestResult({
      tool_name: 'Study Plan Generator Tool',
      action: 'Generated 5-day DBMS exam roadmap',
      result: {
        subject: 'DBMS',
        days: 5,
        daily_hours: 2.5,
        total_study_hours: 12.5,
        plan: [
          { day: 1, focus_topic: 'Relational Model & Keys', duration_hours: 2.5, activities: ['Candidate & Foreign keys', 'Practice 5 identification exercises'] },
          { day: 2, focus_topic: 'Database Normalization (1NF-3NF)', duration_hours: 2.5, activities: ['Decomposition rules', 'BCNF vs 3NF differences'] },
          { day: 3, focus_topic: 'SQL Mastery & Complex Joins', duration_hours: 2.5, activities: ['Inner vs Outer joins', 'Write 10 complex queries'] },
          { day: 4, focus_topic: 'ACID Properties & Transactions', duration_hours: 2.5, activities: ['Conflict serializability', 'Two-phase locking'] },
          { day: 5, focus_topic: 'Indexing & Mock Examination', duration_hours: 2.5, activities: ['B+ trees vs Hash indexing', 'Full timed 20-question test'] }
        ]
      }
    });
  };

  return (
    <div className="flex-1 flex flex-col h-screen bg-slate-950 overflow-y-auto">
      {/* Header */}
      <header className="border-b border-slate-800/90 px-8 py-6 bg-slate-900/40 shrink-0">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
            <Wrench className="w-5 h-5 text-amber-400" />
            Educational Agent Tools Catalog
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Autonomous tools invoked dynamically by the Agentic AI workflow depending on the student's learning intent.
          </p>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto w-full p-8 space-y-8">
        {/* Tool Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {tools.map((t) => (
            <div
              key={t.id}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4 hover:border-slate-700 transition flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-2xl p-2 rounded-xl bg-slate-950 border border-slate-800">
                    {t.icon}
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800/60">
                    {t.status}
                  </span>
                </div>

                <div>
                  <h3 className="font-bold text-sm text-white">{t.name}</h3>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">{t.description}</p>
                </div>

                <div className="space-y-2 pt-2 border-t border-slate-800/80 text-[11px]">
                  <div>
                    <span className="text-slate-500 font-semibold block mb-0.5">Parameters:</span>
                    <div className="flex flex-wrap gap-1">
                      {t.inputs.map((inp, i) => (
                        <span key={i} className="px-1.5 py-0.5 bg-slate-950 text-slate-300 rounded border border-slate-800 font-mono text-[10px]">
                          {inp}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <span className="text-slate-500 font-semibold block mb-0.5">Output Signature:</span>
                    <p className="text-slate-400 text-[11px] leading-snug">{t.output}</p>
                  </div>
                </div>
              </div>

              {/* Action Button */}
              {t.id === 'quiz_generator' && (
                <button
                  onClick={handleRunSampleQuiz}
                  className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold transition"
                >
                  <Play className="w-3.5 h-3.5 text-blue-400" />
                  Test Quiz Generator
                </button>
              )}

              {t.id === 'study_plan' && (
                <button
                  onClick={handleRunSamplePlan}
                  className="w-full flex items-center justify-center gap-1.5 px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold transition"
                >
                  <Play className="w-3.5 h-3.5 text-indigo-400" />
                  Test Study Plan Tool
                </button>
              )}
            </div>
          ))}
        </div>

        {/* Live Interactive Test Playground Area */}
        {testResult && (
          <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="font-bold text-sm text-white flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                Live Tool Execution Output
              </h3>
              <button
                onClick={() => setTestResult(null)}
                className="text-xs text-slate-400 hover:text-slate-200"
              >
                Close Output
              </button>
            </div>

            <ToolResultCard toolResult={testResult} />
          </div>
        )}
      </div>
    </div>
  );
};
