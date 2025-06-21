# GitLab GenAI Chatbot

A sophisticated RAG-powered chatbot that helps users navigate and learn from GitLab's Handbook and Direction pages. Built with transparency and collaboration in mind, following GitLab's "build in public" philosophy.

## 🚀 Features

- **Intelligent Information Retrieval**: Uses RAG (Retrieval Augmented Generation) to provide accurate, contextual answers
- **Real-time Chat Interface**: Modern React-based UI for seamless user interaction
- **GitLab Content Integration**: Automatically processes and indexes GitLab Handbook and Direction pages
- **Advanced Guardrails**: Implements safety measures and transparency features
- **Error Handling**: Robust error handling for smooth user experience
- **Scalable Architecture**: Built with FastAPI and modern Python practices

## 🏗️ Architecture

```
├── backend/                 # FastAPI server with RAG implementation
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   ├── core/           # Core application logic
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic services
│   │   └── utils/          # Utility functions
│   ├── data_processing/    # GitLab content scraping and processing
│   └── requirements.txt
├── frontend/               # React.js user interface
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API integration
│   │   └── styles/         # CSS and styling
│   └── package.json
├── data/                   # Processed GitLab content and embeddings
├── docs/                   # Project documentation
└── tests/                  # Unit and integration tests
```

## 🛠️ Technology Stack

### Backend

- **FastAPI**: High-performance web framework
- **LangChain**: RAG implementation and LLM integration
- **ChromaDB**: Vector database for document embeddings
- **OpenAI/Anthropic**: Language models for chat functionality
- **BeautifulSoup/Scrapy**: Web scraping for GitLab content
- **Pydantic**: Data validation and settings management

### Frontend

- **React.js**: Modern UI framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React Query**: Data fetching and caching
- **React Router**: Client-side routing

### Deployment

- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Vercel/Streamlit Cloud**: Production deployment options

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn
- Git

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd gitlab-genai-chatbot
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DATABASE_URL=sqlite:///./chatbot.db
ENVIRONMENT=development
```

### 4. Data Processing

```bash
# Run the GitLab content scraper
python data_processing/scrape_gitlab.py

# Process and create embeddings
python data_processing/create_embeddings.py
```

### 5. Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Frontend Setup

```bash
cd ../frontend
npm install
npm start
```

### 7. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# For production deployment
docker-compose -f docker-compose.prod.yml up --build
```

## 📚 Usage

1. **Start a Conversation**: Type your question about GitLab's handbook or direction
2. **Get Contextual Answers**: The chatbot retrieves relevant information and provides detailed responses
3. **Follow-up Questions**: Continue the conversation with related queries
4. **Source References**: Each answer includes references to original GitLab documentation

## 🔧 Configuration

### Backend Configuration

Key configuration options in `backend/app/core/config.py`:

- `OPENAI_API_KEY`: OpenAI API key for GPT models
- `ANTHROPIC_API_KEY`: Anthropic API key for Claude models
- `CHUNK_SIZE`: Text chunk size for document processing
- `CHUNK_OVERLAP`: Overlap between text chunks
- `MAX_TOKENS`: Maximum tokens for LLM responses

### Frontend Configuration

Environment variables for React app (`.env.local`):

- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_ENVIRONMENT`: Application environment

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
```

## 📖 API Documentation

The FastAPI backend automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Deployment Options

### Vercel (Recommended for Frontend)

1. Connect your GitHub repository to Vercel
2. Configure build settings for React app
3. Deploy with automatic CI/CD

### Streamlit Community Cloud

1. Upload Streamlit version to GitHub
2. Connect to Streamlit Community Cloud
3. Deploy with one-click

### Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Upload Gradio interface version
3. Deploy with automatic builds

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Voice interface integration
- [ ] Advanced analytics dashboard
- [ ] Integration with GitLab API for real-time updates
- [ ] Mobile app development
- [ ] Custom model fine-tuning

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team.

---

Built with ❤️ following GitLab's "build in public" philosophy
