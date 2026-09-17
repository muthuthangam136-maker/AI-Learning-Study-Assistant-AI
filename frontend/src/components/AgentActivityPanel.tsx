import React from 'react';
import { CheckCircle2, Loader2, Sparkles, Brain, ArrowRight } from 'lucide-react';
import { ActivityStep } from '../types';

interface AgentActivityPanelProps {
  activity: ActivityStep[];
  intent?: string;
  topic?: string;
  status?: string;
  isStreaming?: boolean;
}

export const AgentActivityPanel: React.FC<AgentActivityPanelProps> = ({
  activity,
  intent,
  topic,
  status,
  isStreaming
}) => {
  if (!activity || activity.length === 0) {
    return null;
  }

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-3.5 shadow-sm space-y-3">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <Brain className="w-4 h-4 text-blue-400" />
          <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">
            Agent Execution Activity
          </h4>
        </div>
        <div className="flex items-center gap-1.5 text-[11px]">
          {intent && (
            <span className="px-2 py-0.5 rounded bg-indigo-950/80 text-indigo-300 border border-indigo-800/50 font-medium">
              {intent}
            </span>
          )}
          {topic && topic !== 'Other' && (
            <span className="px-2 py-0.5 rounded bg-blue-950/80 text-blue-300 border border-blue-800/50 font-medium">
              {topic}
            </span>
          )}
        </div>
      </div>

      {/* Steps Timeline */}
      <div className="space-y-2">
        {activity.map((step, idx) => (
          <div key={idx} className="flex items-start gap-2.5 text-xs">
            <div className="mt-0.5">
              {step.status === 'completed' ? (
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              ) : (
                <Loader2 className="w-3.5 h-3.5 text-blue-400 animate-spin shrink-0" />
              )}
            </div>
            <div className="flex-1 flex items-baseline justify-between gap-2">
              <span className="text-slate-300 font-medium">{step.step}</span>
              {step.detail && (
                <span className="text-[11px] text-slate-500 font-mono shrink-0">
                  {step.detail}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Assistance Status footer */}
      {status === 'needs_teacher' && (
        <div className="mt-2 pt-2 border-t border-amber-900/40 text-[11px] text-amber-300 flex items-center gap-1.5">
          <span>⚠️ Low knowledge confidence: Teacher consultation recommended.</span>
        </div>
      )}
    </div>
  );
};
