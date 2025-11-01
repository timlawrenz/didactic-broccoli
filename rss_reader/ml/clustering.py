"""K-Means clustering for user taste profiles."""

import logging
import numpy as np
from typing import Optional, List
from sklearn.cluster import KMeans

from ..db import get_liked_articles
from .vector_store import get_embeddings_for_articles

logger = logging.getLogger(__name__)


def get_taste_centroids(user_id: int = 1, n_clusters: int = 5) -> Optional[np.ndarray]:
    """Calculate taste centroids from liked articles using K-Means.
    
    Args:
        user_id: User ID
        n_clusters: Number of clusters (default 5)
        
    Returns:
        Array of shape (k, 384) with taste centroids, or None if insufficient data
    """
    # Get liked articles
    liked_articles = get_liked_articles(user_id)
    
    if not liked_articles:
        logger.info("No liked articles found")
        return None
    
    if len(liked_articles) < 2:
        logger.info(f"Only {len(liked_articles)} liked article(s), need at least 2 for clustering")
        return None
    
    # Get embeddings for liked articles
    article_ids = [a['article_id'] for a in liked_articles]
    embeddings_dict = get_embeddings_for_articles(article_ids)
    
    if not embeddings_dict:
        logger.warning("No embeddings found for liked articles")
        return None
    
    # Convert to numpy array
    embeddings = np.array([embeddings_dict[aid] for aid in article_ids if aid in embeddings_dict])
    
    if len(embeddings) < 2:
        logger.info(f"Only {len(embeddings)} embedding(s) available, need at least 2")
        return None
    
    # Adjust k if we have fewer articles than clusters
    k = min(n_clusters, len(embeddings))
    
    logger.info(f"Clustering {len(embeddings)} liked articles into {k} taste profiles")
    
    try:
        # Run K-Means clustering
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(embeddings)
        
        centroids = kmeans.cluster_centers_
        
        logger.info(f"Generated {len(centroids)} taste centroids")
        return centroids
        
    except Exception as e:
        logger.error(f"Error running K-Means clustering: {e}")
        return None


def calculate_clusters(embeddings: np.ndarray, k: int = 5) -> Optional[KMeans]:
    """Run K-Means clustering on embeddings.
    
    Args:
        embeddings: Array of shape (n_samples, 384)
        k: Number of clusters
        
    Returns:
        Fitted KMeans model or None if clustering fails
    """
    if len(embeddings) < k:
        k = len(embeddings)
    
    if k < 1:
        return None
    
    try:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(embeddings)
        return kmeans
    except Exception as e:
        logger.error(f"Error in K-Means clustering: {e}")
        return None
