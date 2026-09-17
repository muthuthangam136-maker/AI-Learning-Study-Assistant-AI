import React from 'react';
import { Sparkles } from 'lucide-react';

interface SampleQuestionsProps {
  onSelect: (question: string) => void;
  disabled?: boolean;
}

const SAMPLE_QUESTIONS = [
  "Explain DBMS normalization in simple terms.",
  "I have a DBMS exam in 5 days. Create a study plan.",
  "Quiz me on operating systems.",
  "Explain TCP vs UDP.",
  "Give me 10 Java array practice questions.",
  "I don't understand recursion.",
  "Summarize operating system process management.",
  "Help me prepare for my computer networks exam."
];

export const SampleQuestions: React.FC<SampleQuestionsProps> = ({ onSelect, disabled }) => {
  return (
    <div className="p-4 bg-slate-900/40 border border-slate-800/80 rounded-2xl space-y-2.5">
      <div className="flex items-center gap-2 text-xs font-semibold text-slate-300">
        <Sparkles className="w-4 h-4 text-blue-400" />
        <span>Try Asking an Educational Concept or Triggering a Tool:</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {SAMPLE_QUESTIONS.map((q, idx) => (
          <button
            key={idx}
            disabled={disabled}
            onClick={() => onSelect(q)}
            className="text-xs bg-slate-900 hover:bg-slate-800 active:bg-slate-700 text-slate-300 hover:text-white border border-slate-800 hover:border-blue-500/50 px-3 py-1.5 rounded-full transition disabled:opacity-50 text-left"
          >
            "{q}"
          </button>
        ))}
      </div>
    </div>
  );
};
