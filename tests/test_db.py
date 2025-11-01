"""Tests for database layer."""

import pytest
import sqlite3
from datetime import datetime

from rss_reader.db import connection, models, schema


@pytest.fixture
def db():
    """Create in-memory database for testing."""
    connection.set_database_path(":memory:")
    conn = connection.get_connection()
    yield conn
    connection.close_connection()


class TestFeeds:
    """Test feed operations."""
    
    def test_add_feed(self, db):
        """Test adding a feed."""
        feed_id = models.add_feed("https://example.com/feed", "Example Feed")
        assert feed_id == 1
        
        feed = models.get_feed(feed_id)
        assert feed['url'] == "https://example.com/feed"
        assert feed['name'] == "Example Feed"
    
    def test_add_duplicate_feed(self, db):
        """Test adding duplicate feed raises error."""
        models.add_feed("https://example.com/feed", "Example Feed")
        
        with pytest.raises(sqlite3.IntegrityError):
            models.add_feed("https://example.com/feed", "Duplicate Feed")
    
    def test_get_all_feeds(self, db):
        """Test getting all feeds."""
        models.add_feed("https://example.com/feed1", "Feed 1")
        models.add_feed("https://example.com/feed2", "Feed 2")
        
        feeds = models.get_all_feeds()
        assert len(feeds) == 2
        assert feeds[0]['name'] == "Feed 1"
    
    def test_delete_feed(self, db):
        """Test deleting a feed."""
        feed_id = models.add_feed("https://example.com/feed", "Example Feed")
        models.delete_feed(feed_id)
        
        feed = models.get_feed(feed_id)
        assert feed is None


class TestArticles:
    """Test article operations."""
    
    def test_add_article(self, db):
        """Test adding an article."""
        feed_id = models.add_feed("https://example.com/feed", "Example Feed")
        
        article_id = models.add_article(
            feed_id=feed_id,
            title="Test Article",
            link="https://example.com/article1",
            summary="A test article",
            full_text="Full text content",
            published_date=datetime(2024, 1, 1)
        )
        
        assert article_id == 1
        
        article = models.get_article(article_id)
        assert article['title'] == "Test Article"
        assert article['link'] == "https://example.com/article1"
        assert article['summary'] == "A test article"
        assert article['full_text'] == "Full text content"
    
    def test_add_duplicate_article(self, db):
        """Test adding duplicate article returns None."""
        feed_id = models.add_feed("https://example.com/feed", "Example Feed")
        
        article_id1 = models.add_article(
            feed_id=feed_id,
            title="Test Article",
            link="https://example.com/article1"
        )
        
        article_id2 = models.add_article(
            feed_id=feed_id,
            title="Different Title",
            link="https://example.com/article1"  # Same link
        )
        
        assert article_id1 is not None
        assert article_id2 is None
    
    def test_get_articles_by_feed(self, db):
        """Test getting articles for a feed."""
        feed_id = models.add_feed("https://example.com/feed", "Example Feed")
        
        models.add_article(feed_id, "Article 1", "https://example.com/1")
        models.add_article(feed_id, "Article 2", "https://example.com/2")
        
        articles = models.get_articles_by_feed(feed_id)
        assert len(articles) == 2
    
    def test_cascade_delete(self, db):
        """Test articles are deleted when feed is deleted."""
        feed_id = models.add_feed("https://example.com/feed", "Example Feed")
        article_id = models.add_article(feed_id, "Article", "https://example.com/1")
        
        models.delete_feed(feed_id)
        
        article = models.get_article(article_id)
        assert article is None


class TestUserLikes:
    """Test user interaction operations."""
    
    def test_like_article(self, db):
        """Test liking an article."""
        feed_id = models.add_feed("https://example.com/feed", "Example Feed")
        article_id = models.add_article(feed_id, "Article", "https://example.com/1")
        
        models.like_article(article_id)
        
        liked = models.get_liked_articles()
        assert len(liked) == 1
        assert liked[0]['article_id'] == article_id
    
    def test_like_article_idempotent(self, db):
        """Test liking same article twice is idempotent."""
        feed_id = models.add_feed("https://example.com/feed", "Example Feed")
        article_id = models.add_article(feed_id, "Article", "https://example.com/1")
        
        models.like_article(article_id)
        models.like_article(article_id)  # Like again
        
        liked = models.get_liked_articles()
        assert len(liked) == 1
    
    def test_unlike_article(self, db):
        """Test unliking an article."""
        feed_id = models.add_feed("https://example.com/feed", "Example Feed")
        article_id = models.add_article(feed_id, "Article", "https://example.com/1")
        
        models.like_article(article_id)
        models.unlike_article(article_id)
        
        liked = models.get_liked_articles()
        assert len(liked) == 0
