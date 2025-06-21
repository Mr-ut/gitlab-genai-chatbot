import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ChatInterface } from './components/ChatInterface';
import { Header } from './components/Header';
import './App.css';

// Create a client
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="App min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <ChatInterface />
        </main>
      </div>
    </QueryClientProvider>
  );
}

export default App;
