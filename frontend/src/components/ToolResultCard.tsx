import React, { useState } from 'react';
import { Wrench, CheckCircle, XCircle, Calendar, BookCheck, Award, RefreshCw, Send } from 'lucide-react';
import { ToolExecutionResult } from '../types';
import { api } from '../services/api';

interface ToolResultCardProps {
  toolResult: ToolExecutionResult;
  conversationId?: string;
  onQuizCompleted?: (score: number, total: number) => void;
}

export const ToolResultCard: React.FC<ToolResultCardProps> = ({
  toolResult,
  conversationId,
  onQuizCompleted
}) => {
  const { tool_name, action, result } = toolResult;

  // State for interactive Quiz
  const [userAnswers, setUserAnswers] = useState<Record<number, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!result) return null;

  // 1. Quiz Tool Interactive Card
  if (tool_name === 'Quiz Generator Tool' && result.questions) {
    const questions = result.questions;

    const handleSelect = (qIdx: number, option: string) => {
      if (submitted) return;
      setUserAnswers(prev => ({ ...prev, [qIdx]: option }));
    };

    const handleQuizSubmit = async () => {
      let correctCount = 0;
      questions.forEach((q: any, idx: number) => {
        if (userAnswers[idx] === q.correct_answer) {
          correctCount++;
        }
      });
      setScore(correctCount);
      setSubmitted(true);

      // Save to backend SQLite progress memory
      try {
        setIsSubmitting(true);
        await api.submitQuizScore({
          conversation_id: conversationId,
          subject: result.subject || 'Computer Science',
          topic: result.topic || 'General',
          difficulty: result.difficulty || 'Medium',
          total_questions: questions.length,
          score: correctCount
        });
        if (onQuizCompleted) {
          onQuizCompleted(correctCount, questions.length);
        }
      } catch (err) {
        console.error("Failed to sync quiz score", err);
      } finally {
        setIsSubmitting(false);
      }
    };

    return (
      <div className="bg-slate-900 border border-blue-900/50 rounded-xl p-4 my-3 shadow-lg space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-blue-600/20 text-blue-400">
              <BookCheck className="w-4 h-4" />
            </span>
            <div>
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                Interactive Quiz: {result.subject}
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 font-normal">
                  {result.difficulty}
                </span>
              </h4>
              <p className="text-xs text-slate-400">Select answers and click Submit to record your score</p>
            </div>
          </div>
          {submitted && (
            <div className="flex items-center gap-1 text-xs font-bold px-3 py-1 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-700">
              <Award className="w-3.5 h-3.5" />
              Score: {score} / {questions.length} ({Math.round((score / questions.length) * 100)}%)
            </div>
          )}
        </div>

        {/* Questions list */}
        <div className="space-y-4">
          {questions.map((q: any, qIdx: number) => {
            const chosen = userAnswers[qIdx];
            const isCorrect = chosen === q.correct_answer;

            return (
              <div key={qIdx} className="bg-slate-950/70 border border-slate-800 rounded-lg p-3 space-y-2.5 text-xs">
                <p className="font-semibold text-slate-200">
                  {qIdx + 1}. {q.question}
                </p>
                <div className="space-y-1.5">
                  {q.options.map((opt: string, optIdx: number) => {
                    const isSelected = chosen === opt;
                    let optStyle = 'border-slate-800 bg-slate-900/50 text-slate-300 hover:border-slate-700';

                    if (submitted) {
                      if (opt === q.correct_answer) {
                        optStyle = 'border-emerald-500 bg-emerald-950/40 text-emerald-200 font-semibold';
                      } else if (isSelected && !isCorrect) {
                        optStyle = 'border-rose-500 bg-rose-950/40 text-rose-200';
                      }
                    } else if (isSelected) {
                      optStyle = 'border-blue-500 bg-blue-950/40 text-blue-200 font-semibold';
                    }

                    return (
                      <button
                        key={optIdx}
                        disabled={submitted}
                        onClick={() => handleSelect(qIdx, opt)}
                        className={`w-full text-left px-3 py-2 rounded-md border transition flex items-center justify-between ${optStyle}`}
                      >
                        <span>{opt}</span>
                        {submitted && opt === q.correct_answer && (
                          <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                        )}
                        {submitted && isSelected && !isCorrect && (
                          <XCircle className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                        )}
                      </button>
                    );
                  })}
                </div>

                {/* Explanation shown after submit */}
                {submitted && (
                  <div className="mt-2 pt-2 border-t border-slate-800 text-[11px] text-slate-400 bg-slate-900/40 p-2 rounded">
                    <span className="font-semibold text-blue-400">Explanation: </span>
                    {q.explanation}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Submit Quiz Action */}
        {!submitted && (
          <div className="flex justify-end pt-2">
            <button
              onClick={handleQuizSubmit}
              disabled={Object.keys(userAnswers).length === 0 || isSubmitting}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg text-xs font-semibold shadow-md shadow-blue-600/30 transition"
            >
              <Send className="w-3.5 h-3.5" />
              {isSubmitting ? 'Recording Score...' : 'Submit Answers'}
            </button>
          </div>
        )}
      </div>
    );
  }

  // 2. Study Plan Tool Card
  if (tool_name === 'Study Plan Generator Tool' && result.plan) {
    return (
      <div className="bg-slate-900 border border-indigo-900/50 rounded-xl p-4 my-3 shadow-lg space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-indigo-600/20 text-indigo-400">
              <Calendar className="w-4 h-4" />
            </span>
            <div>
              <h4 className="text-sm font-bold text-white">
                {result.days}-Day Study Roadmap ({result.total_study_hours} hrs total)
              </h4>
              <p className="text-xs text-slate-400">Subject: {result.subject} • {result.daily_hours} hrs/day</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
          {result.plan.map((day: any) => (
            <div key={day.day} className="bg-slate-950/70 border border-slate-800/80 rounded-lg p-3 text-xs space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-bold text-blue-400">Day {day.day}</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">
                  {day.duration_hours}h
                </span>
              </div>
              <p className="font-semibold text-slate-200">{day.focus_topic}</p>
              <ul className="text-[11px] text-slate-400 space-y-0.5 list-disc list-inside">
                {day.activities.map((act: string, idx: number) => (
                  <li key={idx} className="truncate">{act}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // 3. Generic Educational Tool Card
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-3 my-2 text-xs flex items-center justify-between">
      <div className="flex items-center gap-2.5">
        <Wrench className="w-4 h-4 text-amber-400" />
        <div>
          <span className="font-semibold text-slate-200">{tool_name}</span>
          <p className="text-[11px] text-slate-400">{action}</p>
        </div>
      </div>
      <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800/60 font-mono">
        Executed
      </span>
    </div>
  );
};
