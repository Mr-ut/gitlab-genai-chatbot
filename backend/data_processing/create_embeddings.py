"""
Embedding Creation Module

This module processes scraped GitLab content and creates embeddings
for the vector database using ChromaDB and sentence transformers.
"""

import json
import os
import sys
from typing import List, Dict, Any
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.vector_store import vector_store_service
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingProcessor:
    """Process documents and create embeddings for vector storage"""

    def __init__(self):
        self.vector_store = vector_store_service

    def load_scraped_data(self, filepath: str) -> List[Dict[str, Any]]:
        """Load scraped data from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            logger.info(f"Loaded {len(data)} documents from {filepath}")
            return data

        except Exception as e:
            logger.error(f"Error loading scraped data: {e}")
            return []

    def preprocess_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Preprocess documents before creating embeddings"""
        processed_docs = []

        for doc in documents:
            try:
                # Skip documents with insufficient content
                if len(doc.get('content', '')) < 100:
                    continue

                # Clean and validate content
                content = self._clean_content(doc['content'])
                if not content:
                    continue

                processed_doc = {
                    'content': content,
                    'title': doc.get('title', 'Untitled'),
                    'url': doc.get('url', ''),
                    'source': doc.get('url', ''),
                    'metadata': {
                        'scraped_at': doc.get('scraped_at'),
                        'source_type': doc.get('metadata', {}).get('source_type', 'unknown'),
                        'word_count': len(content.split()),
                        'char_count': len(content),
                        **doc.get('metadata', {})
                    }
                }

                processed_docs.append(processed_doc)

            except Exception as e:
                logger.error(f"Error preprocessing document {doc.get('url', 'unknown')}: {e}")
                continue

        logger.info(f"Preprocessed {len(processed_docs)} documents")
        return processed_docs

    def _clean_content(self, content: str) -> str:
        """Clean document content"""
        if not content:
            return ""

        # Remove excessive whitespace
        import re
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'\n\s*\n', '\n\n', content)

        # Remove very short lines that might be navigation or noise
        lines = content.split('\n')
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            # Keep lines that are substantial or are part of lists
            if len(line) > 20 or line.startswith(('- ', '* ', '1. ', '2. ')):
                cleaned_lines.append(line)

        return '\n'.join(cleaned_lines).strip()

    def create_embeddings(self, documents: List[Dict[str, Any]]) -> bool:
        """Create embeddings and store in vector database"""
        try:
            logger.info("Creating embeddings for documents...")

            # Add documents to vector store
            success = self.vector_store.add_documents(documents)

            if success:
                logger.info(f"Successfully created embeddings for {len(documents)} documents")
                return True
            else:
                logger.error("Failed to create embeddings")
                return False

        except Exception as e:
            logger.error(f"Error creating embeddings: {e}")
            return False

    def process_all(self, data_filepath: str) -> Dict[str, Any]:
        """Complete processing pipeline"""
        try:
            # Load scraped data
            raw_documents = self.load_scraped_data(data_filepath)
            if not raw_documents:
                return {"success": False, "error": "No documents loaded"}

            # Preprocess documents
            processed_documents = self.preprocess_documents(raw_documents)
            if not processed_documents:
                return {"success": False, "error": "No valid documents after preprocessing"}

            # Create embeddings
            success = self.create_embeddings(processed_documents)
            if not success:
                return {"success": False, "error": "Failed to create embeddings"}

            # Get final stats
            doc_count = self.vector_store.get_document_count()

            result = {
                "success": True,
                "documents_processed": len(processed_documents),
                "total_documents_in_db": doc_count,
                "processed_at": datetime.utcnow().isoformat(),
                "embedding_model": settings.EMBEDDING_MODEL
            }

            logger.info(f"Processing completed: {result}")
            return result

        except Exception as e:
            logger.error(f"Error in processing pipeline: {e}")
            return {"success": False, "error": str(e)}

def find_latest_scraped_file() -> str:
    """Find the most recent scraped data file"""
    data_dir = "../data"
    if not os.path.exists(data_dir):
        return None

    json_files = [f for f in os.listdir(data_dir) if f.startswith('gitlab_scraped_data_') and f.endswith('.json')]

    if not json_files:
        return None

    # Sort by modification time
    json_files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True)

    return os.path.join(data_dir, json_files[0])

def main():
    """Main function to process embeddings"""
    processor = EmbeddingProcessor()

    # Try to find the latest scraped data file
    data_file = find_latest_scraped_file()

    if not data_file:
        print("No scraped data file found. Please run scrape_gitlab.py first.")
        print("Expected file pattern: ../data/gitlab_scraped_data_*.json")
        return

    print(f"Processing embeddings from: {data_file}")

    # Process all documents
    result = processor.process_all(data_file)

    if result["success"]:
        print("\nEmbedding creation completed successfully!")
        print(f"Documents processed: {result['documents_processed']}")
        print(f"Total documents in database: {result['total_documents_in_db']}")
        print(f"Embedding model: {result['embedding_model']}")
    else:
        print(f"\nEmbedding creation failed: {result['error']}")

if __name__ == "__main__":
    main()
