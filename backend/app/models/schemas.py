from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    model: Optional[str] = Field("gpt-3.5-turbo", description="LLM model to use")
    max_tokens: Optional[int] = Field(500, ge=1, le=2000, description="Maximum tokens in response")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Response creativity")

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str = Field(..., description="Assistant's response")
    conversation_id: str = Field(..., description="Conversation ID")
    sources: List[Dict[str, Any]] = Field(default=[], description="Source documents used")
    metadata: Dict[str, Any] = Field(default={}, description="Response metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DocumentChunk(BaseModel):
    """Document chunk for RAG"""
    content: str = Field(..., description="Document content")
    source: str = Field(..., description="Source URL or identifier")
    title: str = Field(..., description="Document title")
    chunk_id: str = Field(..., description="Unique chunk identifier")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(..., description="Application version")
    dependencies: Dict[str, str] = Field(default={}, description="Dependency status")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(None, description="Request ID for tracking")

class ScrapingResult(BaseModel):
    """Web scraping result model"""
    url: str = Field(..., description="Source URL")
    title: str = Field(..., description="Page title")
    content: str = Field(..., description="Extracted content")
    metadata: Dict[str, Any] = Field(default={}, description="Page metadata")
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

class EmbeddingResult(BaseModel):
    """Embedding creation result"""
    document_id: str = Field(..., description="Document identifier")
    chunks_created: int = Field(..., description="Number of chunks created")
    embedding_model: str = Field(..., description="Embedding model used")
    created_at: datetime = Field(default_factory=datetime.utcnow)
