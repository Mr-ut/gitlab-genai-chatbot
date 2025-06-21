export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  model?: string;
  max_tokens?: number;
  temperature?: number;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  sources: Source[];
  metadata: {
    model_used: string;
    documents_retrieved: number;
    timestamp: string;
  };
}

export interface Source {
  title: string;
  url: string;
  excerpt: string;
  similarity_score: number;
}

export interface Conversation {
  id: string;
  messages: ChatMessage[];
  created_at: Date;
  updated_at: Date;
}

export interface ApiError {
  error: string;
  error_code: string;
  timestamp: string;
  request_id?: string;
}
