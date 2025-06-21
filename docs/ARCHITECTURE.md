# Technical Architecture Documentation

## 🏗️ System Overview

The GitLab GenAI Chatbot is built using a modern RAG (Retrieval Augmented Generation) architecture that combines:

- **Document Retrieval**: Semantic search through GitLab's documentation
- **Language Generation**: AI models for natural language responses
- **Web Interface**: React-based chat interface
- **API Backend**: FastAPI for robust API services

## 📊 Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend│    │   FastAPI Backend│    │  Vector Database│
│                 │    │                  │    │    (ChromaDB)   │
│  ┌─────────────┐│    │ ┌──────────────┐ │    │                 │
│  │Chat Interface││◄──►│ │ Chat Service │ │◄──►│   Embeddings    │
│  └─────────────┘│    │ └──────────────┘ │    │                 │
│                 │    │ ┌──────────────┐ │    └─────────────────┘
│  ┌─────────────┐│    │ │Vector Service│ │           │
│  │UI Components││    │ └──────────────┘ │           │
│  └─────────────┘│    │ ┌──────────────┐ │           │
└─────────────────┘    │ │  LLM Gateway │ │           │
                       │ └──────────────┘ │           │
                       └──────────────────┘           │
                                │                     │
                                ▼                     │
                    ┌─────────────────────┐           │
                    │   External APIs     │           │
                    │ ┌─────────────────┐ │           │
                    │ │   OpenAI GPT    │ │           │
                    │ └─────────────────┘ │           │
                    │ ┌─────────────────┐ │           │
                    │ │Anthropic Claude │ │           │
                    │ └─────────────────┘ │           │
                    └─────────────────────┘           │
                                                      │
                    ┌─────────────────────┐           │
                    │  Data Processing    │───────────┘
                    │ ┌─────────────────┐ │
                    │ │GitLab Scraper   │ │
                    │ └─────────────────┘ │
                    │ ┌─────────────────┐ │
                    │ │Embedding Creator│ │
                    │ └─────────────────┘ │
                    └─────────────────────┘
```

## 🔧 Component Details

### Frontend (React + TypeScript)

**Technology Stack:**

- React 19.1.0 with TypeScript
- Tailwind CSS for styling
- React Query for data fetching
- Axios for HTTP client

**Key Components:**

- `ChatInterface`: Main chat functionality
- `MessageBubble`: Individual message display
- `SourceCard`: Document source references
- `Header`: Application header with navigation

**State Management:**

- React hooks for local state
- React Query for server state
- Context providers for global state

### Backend (FastAPI + Python)

**Technology Stack:**

- FastAPI 0.104.1 for API framework
- Pydantic for data validation
- SQLAlchemy for database ORM
- Uvicorn as ASGI server

**Core Services:**

#### Chat Service (`app/services/chat.py`)

```python
class ChatService:
    def __init__(self):
        self.conversations = {}  # In-memory storage
        self.llm = self._initialize_llm()

    async def chat(self, message, conversation_id, ...):
        # 1. Retrieve relevant documents
        # 2. Build context from documents
        # 3. Generate LLM response
        # 4. Update conversation history
        # 5. Return formatted response
```

#### Vector Store Service (`app/services/vector_store.py`)

```python
class VectorStoreService:
    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings()
        self.vectorstore = Chroma()
        self.text_splitter = RecursiveCharacterTextSplitter()

    def similarity_search(self, query, k=5):
        # Semantic search through document embeddings
```

### Data Processing Pipeline

#### 1. Web Scraping (`data_processing/scrape_gitlab.py`)

```python
class GitLabScraper:
    async def scrape_all(self):
        # 1. Start with base URLs
        # 2. Extract content from pages
        # 3. Follow relevant links
        # 4. Clean and structure data
        # 5. Save to JSON
```

**Scraping Strategy:**

- Asynchronous scraping for performance
- Respectful rate limiting (1 second delay)
- Content filtering and cleaning
- Metadata extraction

#### 2. Embedding Creation (`data_processing/create_embeddings.py`)

```python
class EmbeddingProcessor:
    def process_all(self, data_filepath):
        # 1. Load scraped documents
        # 2. Split into chunks
        # 3. Create embeddings
        # 4. Store in vector database
```

**Chunking Strategy:**

- 1000 characters per chunk
- 200 character overlap
- Preserve document structure
- Maintain source references

### Vector Database (ChromaDB)

**Configuration:**

- Local persistent storage
- Sentence transformer embeddings
- Similarity threshold: 0.7
- Maximum documents per query: 5

**Document Structure:**

```python
{
    "content": "Document text content",
    "metadata": {
        "source": "URL",
        "title": "Page title",
        "source_type": "handbook|direction",
        "chunk_id": "unique_identifier"
    }
}
```

### Language Models Integration

**Supported Models:**

- OpenAI GPT-3.5-turbo, GPT-4
- Anthropic Claude 3 Sonnet
- Fallback to mock responses

**Response Generation:**

```python
async def _generate_response(self, message, context, history):
    prompt = f"""
    System: {self.system_prompt}
    Context: {context}
    History: {formatted_history}
    User: {message}
    """
    return await self.llm.agenerate([prompt])
```

## 🔄 Data Flow

### Chat Request Flow

1. **User Input**: User types message in React frontend
2. **API Request**: Frontend sends POST to `/api/v1/chat`
3. **Document Retrieval**: Backend searches vector database
4. **Context Building**: Relevant documents assembled
5. **LLM Generation**: AI model generates response
6. **Response Return**: Formatted response with sources
7. **UI Update**: Frontend displays response and sources

### Document Processing Flow

1. **Scraping**: Async scraping of GitLab pages
2. **Cleaning**: Text extraction and normalization
3. **Chunking**: Split documents into searchable chunks
4. **Embedding**: Create vector embeddings
5. **Storage**: Store in ChromaDB with metadata

## 🔒 Security Architecture

### API Security

- CORS configuration for cross-origin requests
- Input validation with Pydantic models
- Rate limiting (60 requests/minute)
- Error handling and logging

### Data Security

- No persistent storage of conversations
- API keys secured via environment variables
- Local vector database (no external data sharing)
- Content filtering for sensitive information

## 📈 Performance Characteristics

### Response Times

- Vector search: ~100-200ms
- LLM generation: ~2-5 seconds
- Total response time: ~2-6 seconds

### Scalability

- Stateless backend (easily horizontally scalable)
- Vector database supports distributed deployment
- React frontend serves static files (CDN-friendly)

### Resource Requirements

- Memory: ~1GB for vector database
- CPU: Moderate for embedding computations
- Storage: ~100MB for GitLab documentation embeddings

## 🔄 Error Handling

### Frontend Error Handling

```typescript
const chatMutation = useMutation({
  mutationFn: chatService.sendMessage,
  onError: (error) => {
    // Display user-friendly error message
    // Log error details for debugging
  },
});
```

### Backend Error Handling

```python
@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        result = await chat_service.chat(...)
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="...")
```

## 🧪 Testing Strategy

### Unit Tests

- Service layer testing
- API endpoint testing
- Utility function testing

### Integration Tests

- End-to-end API testing
- Vector database integration
- LLM integration testing

### Frontend Tests

- Component testing with React Testing Library
- User interaction testing
- API integration testing

## 🚀 Deployment Architecture

### Development

```
React Dev Server (3000) ← → FastAPI (8000) ← → ChromaDB
```

### Production

```
Nginx (80/443) → React Build ← → FastAPI → ChromaDB
                      ↓
                 API Proxy (/api)
```

### Docker Containers

- `frontend`: Nginx serving React build
- `backend`: Python FastAPI application
- Shared volumes for data persistence

## 📊 Monitoring and Observability

### Health Checks

- `/api/v1/health`: Service health status
- `/api/v1/status`: Simple status check
- Docker health check configuration

### Logging

- Structured logging with Python logging
- Request/response logging
- Error tracking and alerting

### Metrics (Future Enhancement)

- Prometheus metrics collection
- Response time monitoring
- API usage analytics
- User interaction tracking

## 🔮 Future Architecture Enhancements

### Planned Improvements

1. **Caching Layer**: Redis for response caching
2. **Database**: PostgreSQL for conversation persistence
3. **Authentication**: User accounts and session management
4. **Analytics**: User behavior tracking
5. **Model Fine-tuning**: Custom model training on GitLab data
6. **Multi-tenancy**: Support for multiple organizations
7. **Real-time Updates**: WebSocket for live chat
8. **Mobile App**: React Native mobile application

### Scalability Roadmap

1. **Microservices**: Split into smaller services
2. **Message Queue**: Async processing with Celery/RQ
3. **Load Balancing**: Multiple backend instances
4. **CDN**: Global content delivery
5. **Kubernetes**: Container orchestration
