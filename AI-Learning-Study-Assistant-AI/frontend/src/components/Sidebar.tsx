import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  MessageSquare,
  BookOpen,
  Wrench,
  History,
  BarChart3,
  Info,
  GraduationCap,
  Cpu,
  Database,
  ShieldCheck
} from 'lucide-react';
import { HealthStatus } from '../types';

interface SidebarProps {
  health: HealthStatus | null;
  activeConversationId?: string;
  onNewChat?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ health, onNewChat }) => {
  const isRealAI = health?.operational_mode === 'REAL AI MODE';

  const navItems = [
    { to: '/', label: 'Study Assistant', icon: MessageSquare, badge: null },
    { to: '/knowledge', label: 'Knowledge Base', icon: BookOpen, badge: health?.chroma_chunks ? `${health.chroma_chunks} chunks` : null },
    { to: '/tools', label: 'Learning Tools', icon: Wrench, badge: '5 tools' },
    { to: '/history', label: 'History', icon: History, badge: null },
    { to: '/progress', label: 'Progress', icon: BarChart3, badge: null },
    { to: '/about', label: 'About Project', icon: Info, badge: 'IBM/TNSDC' },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen select-none shrink-0">
      {/* Brand Header */}
      <div className="p-4 border-b border-slate-800">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20 text-white font-bold text-xl">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-sm tracking-tight text-white flex items-center gap-1.5">
              AI Learning
              <span className="text-xs px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 font-mono border border-blue-500/30">AGENT</span>
            </h1>
            <p className="text-xs text-slate-400">Study Assistant</p>
          </div>
        </div>

        {/* New Chat Button */}
        {onNewChat && (
          <button
            onClick={onNewChat}
            className="mt-4 w-full flex items-center justify-center gap-2 px-3 py-2 bg-blue-600 hover:bg-blue-500 active:bg-blue-700 text-white rounded-lg text-xs font-semibold transition shadow-md shadow-blue-600/20"
          >
            <MessageSquare className="w-3.5 h-3.5" />
            + New Study Session
          </button>
        )}
      </div>

      {/* Mode Status Pill */}
      <div className="px-4 py-2.5 bg-slate-950/60 border-b border-slate-800/80">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-medium text-slate-400">Engine Mode:</span>
          {isRealAI ? (
            <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-400 bg-emerald-950/80 border border-emerald-800/60 px-2 py-0.5 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              REAL AI MODE
            </span>
          ) : (
            <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-amber-300 bg-amber-950/80 border border-amber-800/60 px-2 py-0.5 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
              DEMO MODE
            </span>
          )}
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition ${
                  isActive
                    ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`
              }
            >
              <div className="flex items-center gap-2.5">
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="text-[10px] px-1.5 py-0.2 rounded bg-slate-800 text-slate-400 border border-slate-700/60">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* System Information Footer */}
      <div className="p-3 border-t border-slate-800 text-xs bg-slate-950/40 space-y-2">
        <div className="flex items-center justify-between text-[11px] text-slate-400">
          <span className="flex items-center gap-1">
            <Database className="w-3 h-3 text-blue-400" />
            ChromaDB
          </span>
          <span className="text-slate-300 font-mono text-[10px]">Active</span>
        </div>
        <div className="flex items-center justify-between text-[11px] text-slate-400">
          <span className="flex items-center gap-1">
            <Cpu className="w-3 h-3 text-indigo-400" />
            Workflow
          </span>
          <span className="text-slate-300 font-mono text-[10px]">7-Step Agent</span>
        </div>
        <div className="pt-2 border-t border-slate-800/60 text-[10px] text-slate-400 text-center flex items-center justify-center gap-1">
          <ShieldCheck className="w-3 h-3 text-emerald-400" />
          IBM / TNSDC Internship
        </div>
      </div>
    </aside>
  );
};
