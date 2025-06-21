import axios from 'axios';
import { ChatRequest, ChatResponse, Conversation } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://gitlab-genai-chatbot.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatService = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/chat', request);
    return response.data;
  },

  getConversation: async (conversationId: string): Promise<Conversation> => {
    const response = await api.get(`/conversation/${conversationId}`);
    return response.data;
  },

  clearConversation: async (conversationId: string): Promise<void> => {
    await api.delete(`/conversation/${conversationId}`);
  },

  getAvailableModels: async () => {
    const response = await api.get('/models');
    return response.data;
  },

  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};
