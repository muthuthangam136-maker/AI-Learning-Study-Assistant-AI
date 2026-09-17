import React, { useState, useEffect } from 'react';
import { BarChart3, Award, HelpCircle, BookOpen, Clock, TrendingUp, CheckCircle, Flame } from 'lucide-react';
import { api } from '../services/api';
import { ProgressStats } from '../types';

export const ProgressPage: React.FC = () => {
  const [stats, setStats] = useState<ProgressStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      setLoading(true);
      const data = await api.getProgress();
      setStats(data);
    } catch (err) {
      console.error("Failed to load progress metrics", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-screen bg-slate-950 overflow-y-auto">
      {/* Header */}
      <header className="border-b border-slate-800/90 px-8 py-6 bg-slate-900/40 shrink-0">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-xl font-bold text-white flex items-center gap-2.5">
            <BarChart3 className="w-5 h-5 text-emerald-400" />
            Student Learning Progress & Mastery Dashboard
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time analytics aggregating your topics covered, quiz test scores, and learning milestones from SQLite memory.
          </p>
        </div>
      </header>

      {/* Content */}
      <div className="max-w-6xl mx-auto w-full p-8 space-y-8">
        {loading ? (
          <div className="text-center py-16 text-xs text-slate-400">Loading learning analytics...</div>
        ) : !stats || stats.questions_asked_count === 0 ? (
          <div className="text-center py-20 bg-slate-900/40 border border-slate-800 rounded-2xl p-8 space-y-3">
            <Flame className="w-10 h-10 text-slate-600 mx-auto" />
            <h3 className="text-base font-semibold text-slate-200">No learning activity yet.</h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto">
              Ask your first question in the Study Assistant or take a quiz to start building your student progress record!
            </p>
          </div>
        ) : (
          <>
            {/* Top Stat Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2">
                <div className="flex items-center justify-between text-slate-400 text-xs">
                  <span>Questions Asked</span>
                  <HelpCircle className="w-4 h-4 text-blue-400" />
                </div>
                <div className="text-2xl font-bold text-white">{stats.questions_asked_count}</div>
                <p className="text-[11px] text-slate-500">Across {stats.study_sessions_count} study sessions</p>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2">
                <div className="flex items-center justify-between text-slate-400 text-xs">
                  <span>Topics Studied</span>
                  <BookOpen className="w-4 h-4 text-indigo-400" />
                </div>
                <div className="text-2xl font-bold text-white">{stats.topics_studied_count}</div>
                <p className="text-[11px] text-slate-500">Distinct computer science modules</p>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2">
                <div className="flex items-center justify-between text-slate-400 text-xs">
                  <span>Quizzes Completed</span>
                  <Award className="w-4 h-4 text-amber-400" />
                </div>
                <div className="text-2xl font-bold text-white">{stats.quizzes_completed_count}</div>
                <p className="text-[11px] text-slate-500">Evaluated practice assessments</p>
              </div>

              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2">
                <div className="flex items-center justify-between text-slate-400 text-xs">
                  <span>Average Quiz Accuracy</span>
                  <TrendingUp className="w-4 h-4 text-emerald-400" />
                </div>
                <div className="text-2xl font-bold text-emerald-400">{stats.average_quiz_score}%</div>
                <p className="text-[11px] text-slate-500">Overall retention performance</p>
              </div>
            </div>

            {/* Two-Column Analytics */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Subject Breakdown */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
                <h3 className="font-bold text-sm text-white flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-blue-400" />
                  Frequently Studied Subjects
                </h3>
                {Object.keys(stats.subject_breakdown).length === 0 ? (
                  <p className="text-xs text-slate-500">No subject activity recorded yet.</p>
                ) : (
                  <div className="space-y-3">
                    {Object.entries(stats.subject_breakdown).map(([subj, count]) => {
                      const maxVal = Math.max(...Object.values(stats.subject_breakdown), 1);
                      const pct = Math.round((count / maxVal) * 100);

                      return (
                        <div key={subj} className="space-y-1">
                          <div className="flex justify-between text-xs">
                            <span className="font-medium text-slate-300">{subj}</span>
                            <span className="text-slate-400 font-mono">{count} queries</span>
                          </div>
                          <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
                            <div
                              className="bg-gradient-to-r from-blue-600 to-indigo-600 h-full rounded-full transition-all duration-500"
                              style={{ width: `${pct}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* Recent Learning Activity Feed */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
                <h3 className="font-bold text-sm text-white flex items-center gap-2">
                  <Clock className="w-4 h-4 text-indigo-400" />
                  Recent Learning Activity
                </h3>
                {stats.recent_activity.length === 0 ? (
                  <p className="text-xs text-slate-500">No recent activity found.</p>
                ) : (
                  <div className="space-y-3">
                    {stats.recent_activity.map((item) => (
                      <div
                        key={item.id}
                        className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-3 flex items-center justify-between text-xs"
                      >
                        <div className="space-y-0.5">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-slate-200">{item.topic}</span>
                            <span className="text-[10px] px-2 py-0.2 rounded bg-slate-800 text-slate-400">
                              {item.intent}
                            </span>
                          </div>
                          <span className="text-[10px] text-slate-500">{item.date}</span>
                        </div>
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                          item.status === 'needs_teacher'
                            ? 'bg-amber-950 text-amber-400 border border-amber-800/60'
                            : 'bg-emerald-950 text-emerald-400 border border-emerald-800/60'
                        }`}>
                          {item.status === 'needs_teacher' ? 'Assistance' : 'Answered'}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
