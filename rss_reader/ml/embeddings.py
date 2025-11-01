"""Embedding generation using sentence-transformers."""

import logging
import numpy as np
from typing import Optional

logger = logging.getLogger(__name__)

# Global model cache
_model = None


def get_model():
    """Load and cache the sentence-transformers model.
    
    Returns:
        SentenceTransformer model instance
        
    Raises:
        ImportError: If sentence-transformers not installed
    """
    global _model
    
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading sentence-transformers model: all-MiniLM-L6-v2")
            # Force CPU usage
            _model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
            logger.info("Model loaded successfully on CPU")
        except ImportError:
            logger.error("sentence-transformers not installed. Install with: pip install sentence-transformers")
            raise ImportError(
                "sentence-transformers is required for ML features. "
                "Install with: pip install sentence-transformers"
            )
    
    return _model


def prepare_article_text(article: dict) -> str:
    """Prepare article text for embedding generation.
    
    Combines title, summary, and full_text into a single string.
    
    Args:
        article: Article dictionary with title, summary, and full_text
        
    Returns:
        Combined text string
    """
    parts = []
    
    if article.get('title'):
        parts.append(article['title'])
    
    if article.get('summary'):
        parts.append(article['summary'])
    
    if article.get('full_text'):
        parts.append(article['full_text'])
    
    text = " ".join(parts)
    
    # Truncate to reasonable length (models have token limits)
    max_chars = 5000
    if len(text) > max_chars:
        text = text[:max_chars]
    
    return text


def generate_embedding(text: str) -> Optional[np.ndarray]:
    """Generate embedding vector for text.
    
    Args:
        text: Text to embed
        
    Returns:
        384-dimensional numpy array, or None if generation fails
    """
    if not text or not text.strip():
        logger.warning("Empty text provided for embedding")
        return None
    
    try:
        model = get_model()
        embedding = model.encode(text, convert_to_numpy=True)
        
        # Verify embedding shape
        if embedding.shape != (384,):
            logger.error(f"Unexpected embedding shape: {embedding.shape}")
            return None
        
        return embedding
        
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return None


def generate_article_embedding(article: dict) -> Optional[np.ndarray]:
    """Generate embedding for an article.
    
    Convenience function that combines prepare_article_text and generate_embedding.
    
    Args:
        article: Article dictionary
        
    Returns:
        384-dimensional embedding or None if generation fails
    """
    text = prepare_article_text(article)
    return generate_embedding(text)
