"""Tests for ML module."""

import pytest
import numpy as np
import tempfile
import os
from unittest.mock import Mock, patch

from rss_reader.ml import (
    generate_embedding,
    prepare_article_text,
    store_embedding,
    get_embedding,
    get_taste_centroids,
    get_recommendations,
)
from rss_reader.db import add_feed, add_article, like_article
from rss_reader.db.connection import set_database_path, close_connection


@pytest.fixture
def test_db():
    """Create a temporary database for testing."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    
    # Set database path and initialize
    set_database_path(db_path)
    
    # Import to trigger initialization
    from rss_reader.db import get_connection
    get_connection()
    
    yield db_path
    
    # Cleanup
    close_connection()
    if os.path.exists(db_path):
        os.unlink(db_path)


class TestEmbeddings:
    """Test embedding generation."""
    
    def test_prepare_article_text_full(self):
        """Test preparing article text with all fields."""
        article = {
            'title': 'Test Title',
            'summary': 'Test Summary',
            'full_text': 'Test Full Text'
        }
        
        text = prepare_article_text(article)
        assert 'Test Title' in text
        assert 'Test Summary' in text
        assert 'Test Full Text' in text
    
    def test_prepare_article_text_partial(self):
        """Test preparing article text with missing fields."""
        article = {
            'title': 'Test Title',
            'summary': None,
            'full_text': ''
        }
        
        text = prepare_article_text(article)
        assert 'Test Title' in text
        assert len(text) > 0
    
    def test_prepare_article_text_truncation(self):
        """Test text truncation for long articles."""
        article = {
            'title': 'Test',
            'full_text': 'a' * 10000
        }
        
        text = prepare_article_text(article)
        assert len(text) <= 5000
    
    @patch('rss_reader.ml.embeddings.get_model')
    def test_generate_embedding_success(self, mock_get_model):
        """Test successful embedding generation."""
        # Mock the model
        mock_model = Mock()
        mock_embedding = np.random.randn(384).astype(np.float32)
        mock_model.encode.return_value = mock_embedding
        mock_get_model.return_value = mock_model
        
        embedding = generate_embedding("test text")
        
        assert embedding is not None
        assert embedding.shape == (384,)
        assert isinstance(embedding, np.ndarray)
    
    def test_generate_embedding_empty_text(self):
        """Test embedding generation with empty text."""
        embedding = generate_embedding("")
        assert embedding is None
        
        embedding = generate_embedding("   ")
        assert embedding is None


class TestVectorStore:
    """Test vector storage and retrieval."""
    
    def test_store_and_retrieve_embedding(self, test_db):
        """Test storing and retrieving embeddings."""
        # Create a feed and article
        feed_id = add_feed("https://example.com/feed", "Test Feed")
        article_id = add_article(
            feed_id=feed_id,
            title="Test Article",
            link="https://example.com/article",
            summary="Test summary",
            full_text="Test text",
            published_date="2024-01-01"
        )
        
        # Store embedding
        test_embedding = np.random.randn(384).astype(np.float32)
        store_embedding(article_id, test_embedding)
        
        # Retrieve embedding
        retrieved = get_embedding(article_id)
        
        assert retrieved is not None
        assert retrieved.shape == (384,)
        np.testing.assert_array_almost_equal(test_embedding, retrieved)
    
    def test_get_nonexistent_embedding(self, test_db):
        """Test retrieving non-existent embedding."""
        embedding = get_embedding(999999)
        assert embedding is None
    
    def test_store_embedding_invalid_shape(self, test_db):
        """Test storing embedding with invalid shape."""
        feed_id = add_feed("https://example.com/feed", "Test Feed")
        article_id = add_article(
            feed_id=feed_id,
            title="Test Article",
            link="https://example.com/article",
            summary="Test summary",
            full_text="Test text",
            published_date="2024-01-01"
        )
        
        invalid_embedding = np.random.randn(256).astype(np.float32)
        
        with pytest.raises(ValueError):
            store_embedding(article_id, invalid_embedding)


class TestClustering:
    """Test K-Means clustering."""
    
    def test_get_taste_centroids_insufficient_data(self, test_db):
        """Test clustering with insufficient liked articles."""
        centroids = get_taste_centroids(user_id=1)
        assert centroids is None
    
    def test_get_taste_centroids_success(self, test_db):
        """Test successful centroid generation."""
        # Create feed and articles
        feed_id = add_feed("https://example.com/feed", "Test Feed")
        
        # Create 10 articles with embeddings
        article_ids = []
        for i in range(10):
            article_id = add_article(
                feed_id=feed_id,
                title=f"Test Article {i}",
                link=f"https://example.com/article{i}",
                summary=f"Summary {i}",
                full_text=f"Text {i}",
                published_date="2024-01-01"
            )
            article_ids.append(article_id)
            
            # Store random embedding
            embedding = np.random.randn(384).astype(np.float32)
            store_embedding(article_id, embedding)
            
            # Like first 6 articles
            if i < 6:
                like_article(article_id, user_id=1)
        
        # Get centroids
        centroids = get_taste_centroids(user_id=1)
        
        assert centroids is not None
        assert len(centroids) <= 5  # k=5 or fewer if we have < 5 articles
        assert centroids.shape[1] == 384


class TestRecommendations:
    """Test recommendation engine."""
    
    def test_get_recommendations_insufficient_likes(self, test_db):
        """Test recommendations with < 5 liked articles."""
        feed_id = add_feed("https://example.com/feed", "Test Feed")
        
        # Create and like 3 articles
        for i in range(3):
            article_id = add_article(
                feed_id=feed_id,
                title=f"Article {i}",
                link=f"https://example.com/{i}",
                summary="summary",
                full_text="text",
                published_date="2024-01-01"
            )
            like_article(article_id, user_id=1)
        
        # Should return empty list
        recommendations = get_recommendations(user_id=1)
        assert recommendations == []
    
    def test_get_recommendations_success(self, test_db):
        """Test successful recommendation generation."""
        feed_id = add_feed("https://example.com/feed", "Test Feed")
        
        # Create 20 articles with embeddings
        for i in range(20):
            article_id = add_article(
                feed_id=feed_id,
                title=f"Article {i}",
                link=f"https://example.com/{i}",
                summary=f"Summary {i}",
                full_text=f"Text {i}",
                published_date="2024-01-01"
            )
            
            # Store random embedding
            embedding = np.random.randn(384).astype(np.float32)
            store_embedding(article_id, embedding)
            
            # Like first 6 articles
            if i < 6:
                like_article(article_id, user_id=1)
        
        # Get recommendations
        recommendations = get_recommendations(user_id=1, limit=5)
        
        # Should return some recommendations
        assert len(recommendations) > 0
        assert len(recommendations) <= 5
        
        # Check structure
        for rec in recommendations:
            assert 'article_id' in rec
            assert 'title' in rec
            assert 'similarity_score' in rec
            assert 0 <= rec['similarity_score'] <= 1
    
    def test_recommendations_exclude_liked(self, test_db):
        """Test that recommendations exclude already liked articles."""
        feed_id = add_feed("https://example.com/feed", "Test Feed")
        
        liked_ids = []
        for i in range(10):
            article_id = add_article(
                feed_id=feed_id,
                title=f"Article {i}",
                link=f"https://example.com/{i}",
                summary="summary",
                full_text="text",
                published_date="2024-01-01"
            )
            
            embedding = np.random.randn(384).astype(np.float32)
            store_embedding(article_id, embedding)
            
            if i < 6:
                like_article(article_id, user_id=1)
                liked_ids.append(article_id)
        
        recommendations = get_recommendations(user_id=1)
        
        # No recommendations should be liked articles
        recommended_ids = {r['article_id'] for r in recommendations}
        assert not recommended_ids.intersection(set(liked_ids))


class TestCosineSimilarity:
    """Test cosine similarity calculation."""
    
    def test_cosine_similarity_identical(self):
        """Test similarity of identical vectors."""
        from rss_reader.ml.vector_store import cosine_similarity
        
        vec = np.array([1.0, 2.0, 3.0])
        similarity = cosine_similarity(vec, vec)
        
        assert abs(similarity - 1.0) < 0.0001
    
    def test_cosine_similarity_orthogonal(self):
        """Test similarity of orthogonal vectors."""
        from rss_reader.ml.vector_store import cosine_similarity
        
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([0.0, 1.0, 0.0])
        similarity = cosine_similarity(vec1, vec2)
        
        assert abs(similarity) < 0.0001
    
    def test_cosine_similarity_opposite(self):
        """Test similarity of opposite vectors."""
        from rss_reader.ml.vector_store import cosine_similarity
        
        vec1 = np.array([1.0, 2.0, 3.0])
        vec2 = np.array([-1.0, -2.0, -3.0])
        similarity = cosine_similarity(vec1, vec2)
        
        assert abs(similarity - (-1.0)) < 0.0001
