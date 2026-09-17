import axios from 'axios';
import {
  ChatResponse,
  ConversationSummary,
  KnowledgeDocSummary,
  ToolDefinition,
  ProgressStats,
  HealthStatus
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000,
});

export const api = {
  // Health & Mode Check
  async getHealth(): Promise<HealthStatus> {
    const res = await apiClient.get<HealthStatus>('/api/health');
    return res.data;
  },

  // Chat APIs
  async sendMessage(message: string, conversationId?: string, subject?: string): Promise<ChatResponse> {
    const res = await apiClient.post<ChatResponse>('/api/chat', {
      message,
      conversation_id: conversationId,
      subject,
    });
    return res.data;
  },

  async startNewConversation(): Promise<{ conversation_id: string; title: string }> {
    const res = await apiClient.post<{ conversation_id: string; title: string }>('/api/chat/new');
    return res.data;
  },

  // Conversations
  async getConversations(): Promise<ConversationSummary[]> {
    const res = await apiClient.get<ConversationSummary[]>('/api/conversations');
    return res.data;
  },

  async getConversationDetail(id: string): Promise<any> {
    const res = await apiClient.get(`/api/conversations/${id}`);
    return res.data;
  },

  async deleteConversation(id: string): Promise<void> {
    await apiClient.delete(`/api/conversations/${id}`);
  },

  // Knowledge Base
  async getKnowledgeBase(): Promise<KnowledgeDocSummary[]> {
    const res = await apiClient.get<KnowledgeDocSummary[]>('/api/knowledge');
    return res.data;
  },

  async addKnowledgeDoc(data: {
    title: string;
    filename: string;
    subject: string;
    description?: string;
    content: string;
  }): Promise<KnowledgeDocSummary> {
    const res = await apiClient.post<KnowledgeDocSummary>('/api/knowledge', data);
    return res.data;
  },

  async deleteKnowledgeDoc(id: string): Promise<void> {
    await apiClient.delete(`/api/knowledge/${id}`);
  },

  // Tools
  async getTools(): Promise<ToolDefinition[]> {
    const res = await apiClient.get<ToolDefinition[]>('/api/tools');
    return res.data;
  },

  async submitQuizScore(data: {
    conversation_id?: string;
    subject: string;
    topic: string;
    difficulty: string;
    total_questions: number;
    score: number;
  }): Promise<any> {
    const res = await apiClient.post('/api/tools/quiz/submit', data);
    return res.data;
  },

  // Progress Analytics
  async getProgress(): Promise<ProgressStats> {
    const res = await apiClient.get<ProgressStats>('/api/progress');
    return res.data;
  },
};
