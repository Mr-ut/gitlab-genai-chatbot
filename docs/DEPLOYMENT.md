# Deployment Guide

This guide covers different deployment options for the GitLab GenAI Chatbot.

## 🚀 Quick Deployment Options

### 1. Local Development

```bash
# Clone and setup
git clone <repository-url>
cd gitlab-genai-chatbot
./setup.sh

# Start services
docker-compose up --build
```

### 2. Vercel (Frontend Only)

```bash
# Build for production
cd frontend
npm run build

# Deploy to Vercel
npx vercel --prod
```

### 3. Streamlit Community Cloud

Create a Streamlit version for easy deployment:

```python
# streamlit_app.py
import streamlit as st
import requests
import json

st.set_page_config(
    page_title="GitLab GenAI Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 GitLab GenAI Chatbot")
st.markdown("Your AI assistant for GitLab Handbook & Direction")

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about GitLab..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Call your backend API here
            response = "This is a demo response. Connect to your backend API."
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
```

### 4. Hugging Face Spaces

```python
# app.py for Gradio interface
import gradio as gr
import requests

def chat_function(message, history):
    # Your chat logic here
    return "Demo response from GitLab chatbot"

# Create Gradio interface
iface = gr.ChatInterface(
    fn=chat_function,
    title="GitLab GenAI Chatbot",
    description="AI assistant for GitLab Handbook & Direction",
    theme="soft"
)

if __name__ == "__main__":
    iface.launch()
```

## 🐳 Production Deployment with Docker

### Prerequisites

- Docker and Docker Compose
- Domain name (for SSL)
- API keys (OpenAI/Anthropic)

### Steps

1. **Environment Setup**

```bash
# Create production environment file
cp .env.example .env

# Edit with production values
nano .env
```

2. **SSL Certificates**

```bash
# Using Let's Encrypt
mkdir ssl
certbot certonly --standalone -d yourdomain.com
cp /etc/letsencrypt/live/yourdomain.com/* ./ssl/
```

3. **Deploy**

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f
```

## ☁️ Cloud Provider Deployment

### AWS EC2

```bash
# Launch EC2 instance (Ubuntu 22.04)
# Install Docker and Docker Compose

# Clone repository
git clone <repository-url>
cd gitlab-genai-chatbot

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Setup reverse proxy (nginx)
sudo apt install nginx
# Configure nginx with SSL
```

### Google Cloud Run

```yaml
# cloudbuild.yaml
steps:
  # Build backend
  - name: 'gcr.io/cloud-builders/docker'
    args:
      ['build', '-t', 'gcr.io/$PROJECT_ID/gitlab-chatbot-backend', './backend']

  # Build frontend
  - name: 'gcr.io/cloud-builders/docker'
    args:
      [
        'build',
        '-t',
        'gcr.io/$PROJECT_ID/gitlab-chatbot-frontend',
        './frontend',
      ]

  # Push images
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/gitlab-chatbot-backend']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/gitlab-chatbot-frontend']
```

### Azure Container Instances

```bash
# Create resource group
az group create --name gitlab-chatbot --location eastus

# Deploy backend
az container create \
  --resource-group gitlab-chatbot \
  --name backend \
  --image your-registry/gitlab-chatbot-backend \
  --dns-name-label gitlab-chatbot-backend \
  --ports 8000

# Deploy frontend
az container create \
  --resource-group gitlab-chatbot \
  --name frontend \
  --image your-registry/gitlab-chatbot-frontend \
  --dns-name-label gitlab-chatbot-frontend \
  --ports 80
```

## 🔧 Configuration

### Environment Variables

| Variable            | Description         | Required | Default     |
| ------------------- | ------------------- | -------- | ----------- |
| `OPENAI_API_KEY`    | OpenAI API key      | Yes\*    | -           |
| `ANTHROPIC_API_KEY` | Anthropic API key   | Yes\*    | -           |
| `SECRET_KEY`        | JWT secret key      | Yes      | -           |
| `DATABASE_URL`      | Database connection | No       | SQLite      |
| `ENVIRONMENT`       | Environment mode    | No       | development |
| `MAX_PAGES`         | Max pages to scrape | No       | 100         |

\*At least one LLM API key is required

### Performance Tuning

```yaml
# docker-compose.prod.yml adjustments
services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          memory: 512M
    environment:
      - WORKERS=4
```

## 📊 Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8000/api/v1/health

# Frontend health
curl http://localhost:3000
```

### Logging

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Log rotation
docker run --rm -v $(pwd)/logs:/logs logrotate
```

### Metrics

```python
# Add to backend for monitoring
from prometheus_client import Counter, Histogram

CHAT_REQUESTS = Counter('chat_requests_total', 'Total chat requests')
RESPONSE_TIME = Histogram('response_time_seconds', 'Response time')
```

## 🔒 Security

### Production Checklist

- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable security headers
- [ ] Regular security updates
- [ ] Monitor API usage
- [ ] Backup data regularly

### Rate Limiting

```python
# Add to FastAPI app
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/chat")
@limiter.limit("60/minute")
async def chat_endpoint(request: Request, ...):
    # Your code here
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**

   ```bash
   # Fix Python path
   export PYTHONPATH="${PYTHONPATH}:/app"
   ```

2. **Vector Database Issues**

   ```bash
   # Reset ChromaDB
   rm -rf data/chroma_db
   python data_processing/create_embeddings.py
   ```

3. **API Key Issues**

   ```bash
   # Verify API keys
   echo $OPENAI_API_KEY | cut -c1-10
   ```

4. **Memory Issues**
   ```bash
   # Increase Docker memory
   docker system prune
   ```

### Logs and Debugging

```bash
# Detailed logs
docker-compose logs --tail=100 -f

# Debug mode
ENVIRONMENT=development docker-compose up
```
