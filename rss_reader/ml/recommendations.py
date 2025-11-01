"""Recommendation engine combining clustering and vector search."""

import logging
import numpy as np
from typing import List, Dict, Optional

from ..db import get_liked_articles, get_connection
from .clustering import get_taste_centroids
from .vector_store import search_similar, cosine_similarity

logger = logging.getLogger(__name__)


def get_recommendations(user_id: int = 1, limit: int = 50) -> List[Dict]:
    """Get personalized article recommendations.
    
    Args:
        user_id: User ID
        limit: Maximum number of recommendations
        
    Returns:
        List of article dictionaries with similarity scores
    """
    # Get liked articles to exclude from recommendations
    liked_articles = get_liked_articles(user_id)
    liked_ids = {a['article_id'] for a in liked_articles}
    
    # Check minimum liked articles
    if len(liked_ids) < 5:
        logger.info(f"User has only {len(liked_ids)} liked articles, need at least 5")
        return []
    
    # Get taste centroids from K-Means clustering
    centroids = get_taste_centroids(user_id)
    
    if centroids is None or len(centroids) == 0:
        logger.warning("Failed to generate taste centroids")
        return []
    
    logger.info(f"Using {len(centroids)} taste centroids for recommendations")
    
    # Find similar articles for each centroid
    all_candidates = {}  # article_id -> max_similarity
    
    for i, centroid in enumerate(centroids):
        logger.debug(f"Searching for articles similar to centroid {i+1}")
        
        # Search for similar articles
        similar = search_similar(
            centroid,
            limit=limit * 2,  # Get more candidates than needed
            exclude_article_ids=list(liked_ids)
        )
        
        # Track maximum similarity score for each article
        for article_id, similarity in similar:
            if article_id not in all_candidates or similarity > all_candidates[article_id]:
                all_candidates[article_id] = similarity
    
    if not all_candidates:
        logger.info("No candidate articles found")
        return []
    
    # Sort by similarity and get top N
    sorted_candidates = sorted(all_candidates.items(), key=lambda x: x[1], reverse=True)
    top_article_ids = [aid for aid, _ in sorted_candidates[:limit]]
    
    # Fetch article details
    conn = get_connection()
    
    if not top_article_ids:
        return []
    
    placeholders = ",".join("?" * len(top_article_ids))
    cursor = conn.execute(
        f"""
        SELECT a.article_id, a.title, a.link, a.summary, a.published_date, f.name as feed_name
        FROM articles a
        JOIN feeds f ON a.feed_id = f.feed_id
        WHERE a.article_id IN ({placeholders})
        """,
        top_article_ids
    )
    
    # Build result list preserving similarity order
    article_dict = {}
    for row in cursor:
        article_id = row[0]
        article_dict[article_id] = {
            'article_id': article_id,
            'title': row[1],
            'link': row[2],
            'summary': row[3],
            'published_date': row[4],
            'feed_name': row[5],
            'similarity_score': all_candidates[article_id]
        }
    
    # Return in similarity order
    results = [article_dict[aid] for aid in top_article_ids if aid in article_dict]
    
    logger.info(f"Generated {len(results)} recommendations")
    return results


def score_article_similarity(article_embedding: np.ndarray, centroids: np.ndarray) -> float:
    """Calculate similarity score for an article against taste centroids.
    
    Returns the maximum similarity to any centroid.
    
    Args:
        article_embedding: Article embedding vector (384,)
        centroids: Taste centroids array (k, 384)
        
    Returns:
        Maximum similarity score
    """
    max_similarity = 0.0
    
    for centroid in centroids:
        similarity = cosine_similarity(article_embedding, centroid)
        if similarity > max_similarity:
            max_similarity = similarity
    
    return max_similarity
