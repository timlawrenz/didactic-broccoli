"""Vector storage and similarity search in SQLite."""

import logging
import numpy as np
import sqlite3
from typing import Optional, List, Tuple

from ..db import get_connection

logger = logging.getLogger(__name__)


def store_embedding(article_id: int, embedding: np.ndarray) -> None:
    """Store embedding for an article.
    
    Args:
        article_id: Article ID
        embedding: 384-dimensional numpy array
    """
    if embedding.shape != (384,):
        raise ValueError(f"Expected embedding shape (384,), got {embedding.shape}")
    
    conn = get_connection()
    
    # Serialize embedding as bytes
    embedding_bytes = embedding.tobytes()
    
    try:
        conn.execute(
            "INSERT OR REPLACE INTO embeddings (article_id, embedding) VALUES (?, ?)",
            (article_id, embedding_bytes)
        )
        conn.commit()
        logger.debug(f"Stored embedding for article {article_id}")
    except sqlite3.Error as e:
        logger.error(f"Error storing embedding for article {article_id}: {e}")
        raise


def get_embedding(article_id: int) -> Optional[np.ndarray]:
    """Retrieve embedding for an article.
    
    Args:
        article_id: Article ID
        
    Returns:
        384-dimensional numpy array or None if not found
    """
    conn = get_connection()
    
    try:
        cursor = conn.execute(
            "SELECT embedding FROM embeddings WHERE article_id = ?",
            (article_id,)
        )
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        # Deserialize embedding
        embedding_bytes = row[0]
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        
        return embedding
        
    except sqlite3.Error as e:
        logger.error(f"Error retrieving embedding for article {article_id}: {e}")
        return None


def get_embeddings_for_articles(article_ids: List[int]) -> dict[int, np.ndarray]:
    """Get embeddings for multiple articles.
    
    Args:
        article_ids: List of article IDs
        
    Returns:
        Dictionary mapping article_id to embedding
    """
    if not article_ids:
        return {}
    
    conn = get_connection()
    
    # Create placeholders for IN clause
    placeholders = ",".join("?" * len(article_ids))
    
    try:
        cursor = conn.execute(
            f"SELECT article_id, embedding FROM embeddings WHERE article_id IN ({placeholders})",
            article_ids
        )
        
        results = {}
        for row in cursor:
            article_id = row[0]
            embedding_bytes = row[1]
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            results[article_id] = embedding
        
        return results
        
    except sqlite3.Error as e:
        logger.error(f"Error retrieving embeddings: {e}")
        return {}


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Similarity score between -1 and 1
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)


def search_similar(query_embedding: np.ndarray, 
                   limit: int = 50,
                   exclude_article_ids: Optional[List[int]] = None) -> List[Tuple[int, float]]:
    """Find articles similar to query embedding using cosine similarity.
    
    Args:
        query_embedding: 384-dimensional query vector
        limit: Maximum number of results
        exclude_article_ids: Article IDs to exclude from results
        
    Returns:
        List of (article_id, similarity_score) tuples, sorted by similarity descending
    """
    if query_embedding.shape != (384,):
        raise ValueError(f"Expected embedding shape (384,), got {query_embedding.shape}")
    
    conn = get_connection()
    exclude_article_ids = exclude_article_ids or []
    
    try:
        # Get all embeddings
        cursor = conn.execute("SELECT article_id, embedding FROM embeddings")
        
        results = []
        for row in cursor:
            article_id = row[0]
            
            # Skip excluded articles
            if article_id in exclude_article_ids:
                continue
            
            # Deserialize embedding
            embedding_bytes = row[1]
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            
            # Calculate similarity
            similarity = cosine_similarity(query_embedding, embedding)
            results.append((article_id, float(similarity)))
        
        # Sort by similarity descending and limit
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
        
    except sqlite3.Error as e:
        logger.error(f"Error searching similar articles: {e}")
        return []
