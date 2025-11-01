"""Machine learning module for recommendations."""

from .embeddings import generate_embedding, prepare_article_text, get_model, generate_article_embedding
from .vector_store import store_embedding, get_embedding, search_similar
from .clustering import get_taste_centroids
from .recommendations import get_recommendations

__all__ = [
    "generate_embedding",
    "generate_article_embedding",
    "prepare_article_text",
    "get_model",
    "store_embedding",
    "get_embedding",
    "search_similar",
    "get_taste_centroids",
    "get_recommendations",
]
