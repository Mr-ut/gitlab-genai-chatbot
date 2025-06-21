from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings
from app.services.vector_store import vector_store_service
import logging

logger = logging.getLogger(__name__)

class ChatService:
    """Chat service for handling conversations and RAG"""

    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        self.llm = self._initialize_llm()
        self.system_prompt = self._get_system_prompt()

    def _initialize_llm(self):
        """Initialize the language model"""
        try:
            # Try Groq first (free and fast)
            if settings.GROQ_API_KEY and ("llama" in settings.DEFAULT_MODEL.lower() or "mixtral" in settings.DEFAULT_MODEL.lower() or "gemma" in settings.DEFAULT_MODEL.lower()):
                return ChatGroq(
                    model=settings.DEFAULT_MODEL,
                    temperature=settings.TEMPERATURE,
                    max_tokens=settings.MAX_TOKENS,
                    groq_api_key=settings.GROQ_API_KEY
                )
            # Fallback to OpenAI
            elif settings.OPENAI_API_KEY and "gpt" in settings.DEFAULT_MODEL:
                return ChatOpenAI(
                    model_name=settings.DEFAULT_MODEL,
                    temperature=settings.TEMPERATURE,
                    max_tokens=settings.MAX_TOKENS,
                    openai_api_key=settings.OPENAI_API_KEY
                )
            # Fallback to Anthropic
            elif settings.ANTHROPIC_API_KEY and "claude" in settings.DEFAULT_MODEL:
                return ChatAnthropic(
                    model=settings.DEFAULT_MODEL,
                    temperature=settings.TEMPERATURE,
                    max_tokens=settings.MAX_TOKENS,
                    anthropic_api_key=settings.ANTHROPIC_API_KEY
                )
            else:
                logger.warning("No valid API key found, using mock responses")
                return None
        except Exception as e:
            logger.error(f"Error initializing LLM: {e}")
            return None

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the chatbot"""
        return """You are a helpful AI assistant specialized in providing information about GitLab's Handbook and Direction pages.

Your role is to:
1. Answer questions about GitLab's processes, policies, and strategic direction
2. Provide accurate information based on the retrieved documents
3. Be transparent about your sources and limitations
4. Encourage users to visit the original GitLab pages for the most up-to-date information
5. Maintain a professional and helpful tone

Guidelines:
- Always cite your sources when providing information
- If you're not confident about an answer, say so
- Encourage transparency and collaboration, following GitLab's values
- Help users navigate GitLab's extensive documentation
- Be concise but comprehensive in your responses

Remember: You're here to help GitLab employees and community members learn and access information more effectively."""

    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        """Process a chat message and return a response"""
        try:
            # Generate conversation ID if not provided
            if not conversation_id:
                conversation_id = str(uuid.uuid4())

            # Initialize conversation if new
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []

            # Retrieve relevant documents using RAG
            relevant_docs = vector_store_service.similarity_search(
                query=message,
                k=settings.MAX_DOCUMENTS
            )

            # Build context from retrieved documents
            context = self._build_context(relevant_docs)

            # Generate response
            response = await self._generate_response(
                message=message,
                context=context,
                conversation_history=self.conversations[conversation_id],
                model=model,
                max_tokens=max_tokens,
                temperature=temperature
            )

            # Update conversation history
            self.conversations[conversation_id].extend([
                {"role": "user", "content": message, "timestamp": datetime.utcnow()},
                {"role": "assistant", "content": response, "timestamp": datetime.utcnow()}
            ])

            # Prepare sources for response
            sources = self._format_sources(relevant_docs)

            return {
                "response": response,
                "conversation_id": conversation_id,
                "sources": sources,
                "metadata": {
                    "model_used": model or settings.DEFAULT_MODEL,
                    "llm_provider": type(self.llm).__name__ if self.llm else "mock",
                    "documents_retrieved": len(relevant_docs),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }

        except Exception as e:
            logger.error(f"Error in chat service: {e}")
            return {
                "response": "I apologize, but I encountered an error while processing your request. Please try again.",
                "conversation_id": conversation_id or str(uuid.uuid4()),
                "sources": [],
                "metadata": {"error": str(e)}
            }

    def _build_context(self, relevant_docs: List[Dict[str, Any]]) -> str:
        """Build context string from relevant documents"""
        if not relevant_docs:
            return "No relevant documents found in the GitLab Handbook or Direction pages."

        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            context_parts.append(
                f"Document {i}:\n"
                f"Source: {doc['metadata'].get('source', 'Unknown')}\n"
                f"Title: {doc['metadata'].get('title', 'Unknown')}\n"
                f"Content: {doc['content']}\n"
            )

        return "\n---\n".join(context_parts)

    async def _generate_response(
        self,
        message: str,
        context: str,
        conversation_history: List[Dict[str, Any]],
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """Generate a response using the LLM"""
        try:
            if not self.llm:
                return self._get_mock_response(message, context)

            # Build the prompt
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("human", f"""Based on the following context from GitLab's documentation, please answer the user's question:

Context:
{context}

Recent conversation history:
{self._format_conversation_history(conversation_history)}

User question: {message}

Please provide a helpful, accurate response based on the context provided. If the context doesn't contain enough information to answer the question, please say so and suggest where the user might find more information.""")
            ])

            # Generate response
            messages = prompt_template.format_messages()
            response = await self.llm.ainvoke(messages)
            return response.content.strip()

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # Fall back to mock response if LLM fails
            return self._get_mock_response(message, context)

    def _get_mock_response(self, message: str, context: str) -> str:
        """Generate a mock response when no LLM is available"""

        # Extract some content from the context to make the response more relevant
        context_preview = ""
        if context and context != "No relevant documents found in the GitLab Handbook or Direction pages.":
            # Extract first 500 characters from context
            context_preview = context[:500] + "..." if len(context) > 500 else context
            context_preview = context_preview.replace("Document 1:", "").replace("Source:", "").replace("Title:", "").replace("Content:", "")

        return f"""Based on GitLab's documentation, I found relevant information to help answer your question: "{message}"

**Key Information from GitLab's Handbook and Direction pages:**

{context_preview if context_preview else "GitLab is a comprehensive DevSecOps platform that provides a complete set of tools for software development, security, and operations."}

**About GitLab:**
- GitLab is an all-in-one DevSecOps platform that enables teams to collaborate on code, secure applications, and deploy software
- It provides integrated CI/CD, security scanning, project management, and more
- GitLab follows a transparent, values-driven approach with extensive public documentation
- The platform supports both cloud (GitLab.com) and self-managed deployments

**For the most current and detailed information, please visit:**
- 📖 [GitLab Handbook](https://about.gitlab.com/handbook/) - Comprehensive documentation of GitLab's processes and policies
- 🗺️ [GitLab Direction](https://about.gitlab.com/direction/) - Strategic roadmap and product direction
- 💬 [GitLab Documentation](https://docs.gitlab.com/) - Technical documentation and guides

*Note: I'm currently running in demo mode. For production use, please configure valid API keys for enhanced AI responses.*

Is there a specific aspect of GitLab you'd like to know more about?"""

    def _format_conversation_history(self, history: List[Dict[str, Any]]) -> str:
        """Format conversation history for context"""
        if not history:
            return "No previous conversation."

        formatted = []
        for msg in history[-6:]:  # Last 6 messages for context
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            formatted.append(f"{role.capitalize()}: {content[:200]}...")

        return "\n".join(formatted)

    def _format_sources(self, relevant_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format sources for the response"""
        sources = []
        for doc in relevant_docs:
            sources.append({
                "title": doc['metadata'].get('title', 'Unknown'),
                "url": doc['metadata'].get('source', ''),
                "excerpt": doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content'],
                "similarity_score": doc.get('similarity_score', 0.0)
            })
        return sources

    def get_conversation(self, conversation_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get conversation history"""
        return self.conversations.get(conversation_id)

    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

# Global chat service instance
chat_service = ChatService()
