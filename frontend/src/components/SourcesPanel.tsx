import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp, ExternalLink, Percent } from 'lucide-react';
import { SourceItem } from '../types';

interface SourcesPanelProps {
  sources: SourceItem[];
}

export const SourcesPanel: React.FC<SourcesPanelProps> = ({ sources }) => {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);

  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-3 shadow-sm space-y-2">
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-emerald-400" />
          <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">
            Grounded Knowledge Sources ({sources.length})
          </h4>
        </div>
        <span className="text-[10px] text-slate-500 font-mono">ChromaDB RAG</span>
      </div>

      <div className="space-y-1.5">
        {sources.map((src, idx) => {
          const isExpanded = expandedIndex === idx;
          const matchPercent = Math.round(src.relevance * 100);

          return (
            <div
              key={idx}
              className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-2 text-xs transition hover:border-slate-700"
            >
              <div
                className="flex items-center justify-between cursor-pointer"
                onClick={() => setExpandedIndex(isExpanded ? null : idx)}
              >
                <div className="flex items-center gap-2 overflow-hidden">
                  <span className="font-semibold text-slate-200 truncate">{src.title}</span>
                  <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-400 shrink-0">
                    {src.filename}
                  </span>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                    matchPercent >= 80
                      ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/50'
                      : 'bg-blue-950 text-blue-400 border border-blue-800/50'
                  }`}>
                    {matchPercent}% match
                  </span>
                  {isExpanded ? (
                    <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                  )}
                </div>
              </div>

              {src.section && (
                <div className="text-[11px] text-slate-400 mt-1 font-medium">
                  Section: {src.section}
                </div>
              )}

              {isExpanded && src.excerpt && (
                <div className="mt-2 pt-2 border-t border-slate-800 text-[11px] text-slate-300 bg-slate-900/50 p-2 rounded leading-relaxed font-sans">
                  {src.excerpt}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
