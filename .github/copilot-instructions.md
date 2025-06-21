# Copilot Instructions for GitLab GenAI Chatbot

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview

This is a GenAI chatbot project that retrieves information from GitLab's Handbook and Direction pages using RAG (Retrieval Augmented Generation) architecture.

## Key Technologies

- **Backend**: Python FastAPI with LangChain for RAG implementation
- **Frontend**: React.js with modern UI components
- **Vector Database**: ChromaDB for document embeddings
- **AI Models**: OpenAI GPT or Anthropic Claude for chat functionality
- **Web Scraping**: BeautifulSoup and Scrapy for data collection

## Code Guidelines

- Follow Python PEP 8 standards for backend code
- Use TypeScript for React frontend components
- Implement proper error handling and logging
- Add comprehensive documentation for all functions
- Use environment variables for API keys and configuration
- Implement rate limiting and security best practices

## Architecture Patterns

- Use dependency injection for FastAPI services
- Implement proper separation of concerns
- Use async/await patterns for API calls
- Follow REST API conventions
- Implement proper data validation with Pydantic models
