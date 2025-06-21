import { useMutation } from '@tanstack/react-query';
import React, { useEffect, useRef, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { chatService } from '../services/api';
import { ChatMessage, ChatRequest, Source } from '../types';
import { LoadingSpinner } from './LoadingSpinner';
import { MessageBubble } from './MessageBubble';
import { SourceCard } from './SourceCard';

export const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<string>('');
  const [sources, setSources] = useState<Source[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize conversation ID
  useEffect(() => {
    setConversationId(uuidv4());
  }, []);

  const chatMutation = useMutation({
    mutationFn: (request: ChatRequest) => chatService.sendMessage(request),
    onSuccess: (response) => {
      // Add assistant message
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setSources(response.sources);
      setConversationId(response.conversation_id);
    },
    onError: (error) => {
      console.error('Chat error:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'I apologize, but I encountered an error while processing your request. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim() || chatMutation.isPending) return;

    // Add user message immediately
    const userMessage: ChatMessage = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    // Send to API
    const request: ChatRequest = {
      message: input.trim(),
      conversation_id: conversationId || undefined,
    };

    chatMutation.mutate(request);
    setInput('');
    setSources([]); // Clear previous sources
  };

  const handleClearChat = () => {
    setMessages([]);
    setSources([]);
    setConversationId(uuidv4());
  };

  const handleExampleClick = (example: string) => {
    setInput(example);
  };

  const exampleQuestions = [
    "What is GitLab's remote work policy?",
    "How does GitLab handle code reviews?",
    "What are GitLab's company values?",
    "Tell me about GitLab's product strategy",
    "How does GitLab approach diversity and inclusion?",
  ];

  return (
    <div className="max-w-4xl mx-auto">
      {/* Welcome Section */}
      {messages.length === 0 && (
        <div className="text-center mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Welcome to GitLab GenAI Chatbot
            </h2>
            <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
              I'm here to help you navigate GitLab's extensive Handbook and Direction pages.
              Ask me anything about GitLab's processes, policies, values, or strategic direction.
            </p>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="font-semibold text-blue-900 mb-2">📚 Handbook</h3>
                <p className="text-sm text-blue-700">
                  Processes, policies, and how we work at GitLab
                </p>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <h3 className="font-semibold text-purple-900 mb-2">🎯 Direction</h3>
                <p className="text-sm text-purple-700">
                  Product strategy and future roadmap
                </p>
              </div>
            </div>
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Try asking:</h3>
            <div className="grid gap-2 md:grid-cols-1">
              {exampleQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(question)}
                  className="text-left p-3 bg-white border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                >
                  <span className="text-blue-600">💬</span> {question}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Chat Messages */}
      {messages.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="p-4 border-b border-gray-200 flex justify-between items-center">
            <h3 className="font-semibold text-gray-900">Conversation</h3>
            <button
              onClick={handleClearChat}
              className="text-sm text-gray-500 hover:text-red-600 transition-colors"
            >
              Clear Chat
            </button>
          </div>

          <div className="p-4 max-h-96 overflow-y-auto">
            {messages.map((message, index) => (
              <MessageBubble key={index} message={message} />
            ))}

            {chatMutation.isPending && (
              <div className="flex justify-start mb-4">
                <div className="bg-gray-100 rounded-lg p-3 max-w-xs">
                  <LoadingSpinner />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>
      )}

      {/* Sources */}
      {sources.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6">
          <div className="p-4 border-b border-gray-200">
            <h3 className="font-semibold text-gray-900">Sources</h3>
            <p className="text-sm text-gray-600">Information retrieved from GitLab documentation</p>
          </div>
          <div className="p-4 grid gap-4 md:grid-cols-2">
            {sources.map((source, index) => (
              <SourceCard key={index} source={source} />
            ))}
          </div>
        </div>
      )}

      {/* Chat Input */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <form onSubmit={handleSubmit} className="p-4">
          <div className="flex space-x-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything about GitLab..."
              className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={chatMutation.isPending}
            />
            <button
              type="submit"
              disabled={!input.trim() || chatMutation.isPending}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {chatMutation.isPending ? (
                <LoadingSpinner size="sm" />
              ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              )}
            </button>
          </div>

          <div className="mt-2 text-xs text-gray-500">
            Press Enter to send • This chatbot uses GitLab's public documentation
          </div>
        </form>
      </div>
    </div>
  );
};
