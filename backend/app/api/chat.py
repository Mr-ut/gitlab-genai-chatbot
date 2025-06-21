from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from app.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.services.chat import chat_service
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for processing user messages"""
    try:
        # Validate request
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Process chat request
        result = await chat_service.chat(
            message=request.message,
            conversation_id=request.conversation_id,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        return ChatResponse(**result)

    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

@router.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    try:
        conversation = chat_service.get_conversation(conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return {"conversation_id": conversation_id, "messages": conversation}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving conversation")

@router.delete("/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear conversation history"""
    try:
        success = chat_service.clear_conversation(conversation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return {"message": "Conversation cleared successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(status_code=500, detail="Error clearing conversation")

@router.get("/models")
async def list_available_models():
    """List available chat models"""
    models = [
        {
            "id": "gpt-3.5-turbo",
            "name": "GPT-3.5 Turbo",
            "provider": "OpenAI",
            "available": bool(settings.OPENAI_API_KEY)
        },
        {
            "id": "gpt-4",
            "name": "GPT-4",
            "provider": "OpenAI",
            "available": bool(settings.OPENAI_API_KEY)
        },
        {
            "id": "claude-3-sonnet",
            "name": "Claude 3 Sonnet",
            "provider": "Anthropic",
            "available": bool(settings.ANTHROPIC_API_KEY)
        }
    ]

    return {"models": models, "default": settings.DEFAULT_MODEL}
