import uuid
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Try to import ChromaDB, handle failure gracefully (e.g. Python 3.14 incompatibility)
try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except Exception as e:
    logger.warning(f"ChromaDB could not be imported (likely Python 3.14 incompatibility): {e}")
    CHROMA_AVAILABLE = False

class MemoryService:
    def __init__(self):
        self.collection = None
        self.local_memory = [] # Fallback in-memory storage

        if CHROMA_AVAILABLE:
            try:
                # Persistent client in valid directory
                self.client = chromadb.PersistentClient(path="./chroma_db_storage")
                self.collection = self.client.get_or_create_collection(name="emotional_context")
                logger.info("Memory service initialized with ChromaDB.")
            except Exception as e:
                logger.error(f"Failed to initialize ChromaDB client: {e}")
                self.collection = None
        else:
            logger.warning("Using in-memory fallback for Emotional Memory (non-persistent).")

    def add_memory(self, user_id: str, text: str, emotion: str, confidence: float):
        metadata = {
            "user_id": user_id,
            "text": text,
            "emotion": emotion,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        }

        if self.collection:
            try:
                pk = str(uuid.uuid4())
                self.collection.add(
                    documents=[text],
                    metadatas=[{k: v for k, v in metadata.items() if k != "text"}], # text is document
                    ids=[pk]
                )
            except Exception as e:
                logger.error(f"Error adding memory to ChromaDB: {e}")
        else:
            # Fallback
            self.local_memory.append(metadata)

    def get_context(self, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        context = []
        
        if self.collection:
            try:
                results = self.collection.query(
                    query_texts=[""], # Dummy query
                    where={"user_id": user_id},
                    n_results=limit
                )
                
                if results['documents']:
                    docs = results['documents'][0]
                    metas = results['metadatas'][0]
                    
                    for doc, meta in zip(docs, metas):
                        context.append({
                            "text": doc,
                            "emotion": meta['emotion'],
                            "confidence": meta['confidence'],
                            "timestamp": meta['timestamp']
                        })
            except Exception as e:
                logger.error(f"Error retrieving context from ChromaDB: {e}")
                
        else:
            # Fallback: simple filter (reverse chronological)
            user_memories = [m for m in self.local_memory if m["user_id"] == user_id]
            # Sort by timestamp desc (newest first)
            user_memories.sort(key=lambda x: x["timestamp"], reverse=True)
            context = user_memories[:limit]
            
        return context

memory_service = MemoryService()
