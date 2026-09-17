export interface ActivityStep {
  step: string;
  status: 'pending' | 'in_progress' | 'completed' | 'warning';
  detail?: string;
}

export interface SourceItem {
  title: string;
  filename: string;
  section?: string;
  relevance: number;
  excerpt?: string;
}

export interface ToolExecutionResult {
  tool_name: string;
  action: string;
  result: any;
  timestamp?: string;
}

export interface ChatResponse {
  conversation_id: string;
  message: string;
  intent: string;
  topic: string;
  status: 'answered' | 'learning' | 'needs_teacher';
  tools_used: ToolExecutionResult[];
  sources: SourceItem[];
  activity: ActivityStep[];
  memory_updated: boolean;
  suggested_followups: string[];
  created_at: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  intent?: string;
  topic?: string;
  status?: 'answered' | 'learning' | 'needs_teacher';
  tools_used?: ToolExecutionResult[];
  sources?: SourceItem[];
  activity?: ActivityStep[];
  suggested_followups?: string[];
  created_at: string;
}

export interface ConversationSummary {
  id: string;
  title: string;
  subject: string;
  message_count: number;
  created_at: string;
  updated_at: string;
}

export interface KnowledgeDocSummary {
  id: string;
  title: string;
  filename: string;
  subject: string;
  description?: string;
  chunks_count: number;
  created_at: string;
}

export interface ToolDefinition {
  id: string;
  name: string;
  icon: string;
  description: string;
  inputs: string[];
  output: string;
  status: string;
}

export interface ProgressStats {
  topics_studied_count: number;
  questions_asked_count: number;
  quizzes_completed_count: number;
  average_quiz_score: number;
  study_sessions_count: number;
  recent_activity: Array<{
    id: string;
    topic: string;
    intent: string;
    status: string;
    date: string;
  }>;
  subject_breakdown: Record<string, number>;
}

export interface HealthStatus {
  status: string;
  project: string;
  version: string;
  demo_mode: boolean;
  operational_mode: 'REAL AI MODE' | 'DEMO MODE';
  llm_model: string;
  chroma_chunks: number;
  vector_store_active: boolean;
  agentic_workflow: string;
}
