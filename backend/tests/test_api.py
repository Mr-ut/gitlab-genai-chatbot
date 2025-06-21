import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "dependencies" in data

def test_status_endpoint():
    """Test simple status endpoint"""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "timestamp" in data

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "GitLab GenAI Chatbot API"
    assert data["version"] == "1.0.0"
    assert data["docs"] == "/docs"

def test_chat_endpoint_empty_message():
    """Test chat endpoint with empty message"""
    response = client.post("/api/v1/chat", json={
        "message": ""
    })
    assert response.status_code == 400

def test_chat_endpoint_valid_message():
    """Test chat endpoint with valid message"""
    response = client.post("/api/v1/chat", json={
        "message": "What is GitLab?"
    })
    # Should return 200 even if no LLM is configured (mock response)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "conversation_id" in data
    assert "sources" in data
    assert "metadata" in data

def test_models_endpoint():
    """Test available models endpoint"""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert "default" in data
    assert len(data["models"]) > 0

def test_conversation_not_found():
    """Test getting non-existent conversation"""
    response = client.get("/api/v1/conversation/nonexistent")
    assert response.status_code == 404
