from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores.utils import filter_complex_metadata
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class VectorStoreService:
    """Vector store service for document embeddings and retrieval"""

    def __init__(self):
        self.embeddings = SentenceTransformerEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.vectorstore = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Initialize ChromaDB vector store"""
        try:
            self.vectorstore = Chroma(
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                embedding_function=self.embeddings
            )
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise

    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to the vector store"""
        try:
            # Convert documents to LangChain Document format
            langchain_docs = []
            for doc in documents:
                # Split document into chunks
                chunks = self.text_splitter.split_text(doc["content"])

                for i, chunk in enumerate(chunks):
                    metadata = {
                        "source": doc.get("source", ""),
                        "title": doc.get("title", ""),
                        "chunk_id": f"{doc.get('url', '')}_{i}",
                        "scraped_at": doc.get("scraped_at", datetime.utcnow().isoformat()),
                    }

                    # Add simple metadata fields only (str, int, float, bool, None)
                    doc_metadata = doc.get("metadata", {})
                    for key, value in doc_metadata.items():
                        if isinstance(value, (str, int, float, bool, type(None))):
                            metadata[key] = value

                    langchain_docs.append(Document(page_content=chunk, metadata=metadata))

            # Add to vector store
            if langchain_docs:
                # Filter complex metadata that ChromaDB doesn't support
                filtered_docs = filter_complex_metadata(langchain_docs)
                self.vectorstore.add_documents(filtered_docs)
                self.vectorstore.persist()
                logger.info(f"Added {len(filtered_docs)} document chunks to vector store")
                return True

            return False
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            return False

    def similarity_search(
        self,
        query: str,
        k: int = None,
        filter_metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            k = k or settings.MAX_DOCUMENTS

            # Perform similarity search
            results = self.vectorstore.similarity_search_with_score(
                query,
                k=k,
                filter=filter_metadata
            )

            # Format results
            formatted_results = []
            for doc, score in results:
                # Note: Lower scores mean higher similarity in some distance metrics
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": score
                })

            logger.info(f"Found {len(formatted_results)} relevant documents for query")
            return formatted_results

        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            return []

    def get_document_count(self) -> int:
        """Get total number of documents in the vector store"""
        try:
            # This is a simplified count - ChromaDB doesn't have a direct count method
            return self.vectorstore._collection.count()
        except Exception as e:
            logger.error(f"Error getting document count: {e}")
            return 0

    def delete_documents(self, filter_metadata: Dict[str, Any] = None) -> bool:
        """Delete documents from vector store"""
        try:
            if filter_metadata:
                # Delete with filter
                self.vectorstore.delete(where=filter_metadata)
            else:
                # Clear all documents
                self.vectorstore.delete_collection()
                self._initialize_vectorstore()

            self.vectorstore.persist()
            logger.info("Documents deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return False

# Global vector store instance
vector_store_service = VectorStoreService()
