import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, Clock, Tag, BookOpen, AlertTriangle } from 'lucide-react';
import { ChatMessage } from '../types';
import { AgentActivityPanel } from './AgentActivityPanel';
import { SourcesPanel } from './SourcesPanel';
import { ToolResultCard } from './ToolResultCard';

interface ChatBubbleProps {
  message: ChatMessage;
  onFollowupClick?: (text: string) => void;
  onQuizCompleted?: (score: number, total: number) => void;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({
  message,
  onFollowupClick,
  onQuizCompleted
}) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-3 my-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {/* Bot Avatar */}
      {!isUser && (
        <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shrink-0 shadow-md shadow-blue-500/20">
          <Bot className="w-4 h-4" />
        </div>
      )}

      <div className={`max-w-[85%] md:max-w-[78%] space-y-3 ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Main Message Bubble */}
        <div
          className={`rounded-2xl px-4 py-3.5 shadow-sm text-sm ${
            isUser
              ? 'bg-blue-600 text-white rounded-br-xs'
              : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-xs'
          }`}
        >
          {/* Metadata Header for Assistant messages */}
          {!isUser && (message.intent || message.topic) && (
            <div className="flex flex-wrap items-center gap-2 mb-2.5 pb-2 border-b border-slate-800 text-[11px]">
              {message.topic && message.topic !== 'Other' && (
                <span className="flex items-center gap-1 font-semibold text-blue-400">
                  <Tag className="w-3 h-3" />
                  {message.topic}
                </span>
              )}
              {message.intent && (
                <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
                  {message.intent}
                </span>
              )}
              {message.status === 'needs_teacher' && (
                <span className="flex items-center gap-1 px-2 py-0.5 rounded bg-amber-950/80 text-amber-300 border border-amber-800/60 font-semibold">
                  <AlertTriangle className="w-3 h-3 text-amber-400" />
                  Teacher Assistance
                </span>
              )}
            </div>
          )}

          {/* Markdown Content */}
          <div className="prose-custom break-words leading-relaxed">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        </div>

        {/* Tools Executed Cards */}
        {!isUser && message.tools_used && message.tools_used.length > 0 && (
          <div className="space-y-2 w-full">
            {message.tools_used.map((tool, idx) => (
              <ToolResultCard
                key={idx}
                toolResult={tool}
                conversationId={message.id}
                onQuizCompleted={onQuizCompleted}
              />
            ))}
          </div>
        )}

        {/* Grounded Knowledge Sources */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="w-full">
            <SourcesPanel sources={message.sources} />
          </div>
        )}

        {/* Agent Activity Trace */}
        {!isUser && message.activity && message.activity.length > 0 && (
          <div className="w-full">
            <AgentActivityPanel
              activity={message.activity}
              intent={message.intent}
              topic={message.topic}
              status={message.status}
            />
          </div>
        )}

        {/* Suggested Follow-up Prompts */}
        {!isUser && message.suggested_followups && message.suggested_followups.length > 0 && onFollowupClick && (
          <div className="flex flex-wrap gap-1.5 pt-1">
            <span className="text-[11px] text-slate-400 w-full mb-0.5">Suggested Next Questions:</span>
            {message.suggested_followups.map((followup, idx) => (
              <button
                key={idx}
                onClick={() => onFollowupClick(followup)}
                className="text-xs bg-slate-800/80 hover:bg-slate-700 text-blue-300 hover:text-blue-200 border border-blue-900/40 px-2.5 py-1 rounded-full transition"
              >
                + {followup}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-200 shrink-0">
          <User className="w-4 h-4" />
        </div>
      )}
    </div>
  );
};
