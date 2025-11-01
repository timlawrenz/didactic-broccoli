"""Integration tests for end-to-end workflows."""

import pytest
from unittest.mock import patch, Mock
from io import BytesIO

from rss_reader.db import connection, models
from rss_reader.fetcher import pipeline
from tests.fixtures.sample_feed import SAMPLE_RSS


@pytest.fixture
def db():
    """Create in-memory database for testing."""
    connection.set_database_path(":memory:")
    conn = connection.get_connection()
    yield conn
    connection.close_connection()


class TestEndToEnd:
    """Test complete fetch and store workflow."""
    
    @patch('rss_reader.fetcher.article_extractor.Article')
    @patch('rss_reader.fetcher.feed_parser.feedparser.parse')
    def test_fetch_and_store_feed(self, mock_parse, mock_article_class, db):
        """Test complete fetch and store pipeline."""
        # Setup: Add feed
        feed_id = models.add_feed("https://example.com/feed", "Test Feed")
        
        # Mock feedparser
        mock_feed = Mock()
        mock_feed.status = 200
        mock_feed.bozo = False
        
        # Create mock entries
        mock_entry1 = Mock()
        mock_entry1.title = "Test Article 1"
        mock_entry1.link = "https://example.com/article1"
        mock_entry1.summary = "Article 1 summary"
        mock_entry1.published_parsed = (2024, 1, 1, 12, 0, 0, 0, 1, 0)
        
        mock_entry2 = Mock()
        mock_entry2.title = "Test Article 2"
        mock_entry2.link = "https://example.com/article2"
        mock_entry2.summary = "Article 2 summary"
        mock_entry2.published_parsed = (2024, 1, 2, 12, 0, 0, 0, 1, 0)
        
        mock_feed.entries = [mock_entry1, mock_entry2]
        mock_parse.return_value = mock_feed
        
        # Mock article extraction
        mock_article1 = Mock()
        mock_article1.text = "Full text 1"
        mock_article2 = Mock()
        mock_article2.text = "Full text 2"
        mock_article_class.side_effect = [mock_article1, mock_article2]
        
        # Execute: Fetch and store
        new_count = pipeline.fetch_and_store_feed(feed_id)
        
        # Verify: 2 articles added
        assert new_count == 2
        
        articles = models.get_articles_by_feed(feed_id)
        assert len(articles) == 2
        assert articles[0]['title'] == "Test Article 2"  # Sorted by date DESC
        assert articles[0]['full_text'] == "Full text 2"
        assert articles[1]['title'] == "Test Article 1"
    
    @patch('rss_reader.fetcher.article_extractor.Article')
    @patch('rss_reader.fetcher.feed_parser.feedparser.parse')
    def test_fetch_idempotency(self, mock_parse, mock_article_class, db):
        """Test re-fetching doesn't create duplicates."""
        feed_id = models.add_feed("https://example.com/feed", "Test Feed")
        
        # Setup mock feed
        mock_feed = Mock()
        mock_feed.status = 200
        mock_feed.bozo = False
        
        mock_entry = Mock()
        mock_entry.title = "Test Article"
        mock_entry.link = "https://example.com/article1"
        mock_entry.summary = "Test summary"
        mock_entry.published_parsed = (2024, 1, 1, 12, 0, 0, 0, 1, 0)
        
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        # Mock article extraction
        mock_article = Mock()
        mock_article.text = "Full text"
        mock_article_class.return_value = mock_article
        
        # First fetch
        new_count1 = pipeline.fetch_and_store_feed(feed_id)
        assert new_count1 == 1
        
        # Second fetch (same articles)
        new_count2 = pipeline.fetch_and_store_feed(feed_id)
        assert new_count2 == 0
        
        # Verify only one article in database
        articles = models.get_articles_by_feed(feed_id)
        assert len(articles) == 1
    
    @patch('rss_reader.fetcher.article_extractor.Article')
    @patch('rss_reader.fetcher.feed_parser.feedparser.parse')
    def test_extraction_failure_fallback(self, mock_parse, mock_article_class, db):
        """Test graceful degradation when article extraction fails."""
        feed_id = models.add_feed("https://example.com/feed", "Test Feed")
        
        # Setup mock feed
        mock_feed = Mock()
        mock_feed.status = 200
        mock_feed.bozo = False
        
        mock_entry = Mock()
        mock_entry.title = "Test Article"
        mock_entry.link = "https://example.com/article1"
        mock_entry.summary = "Test summary"
        mock_entry.published_parsed = (2024, 1, 1, 12, 0, 0, 0, 1, 0)
        
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        # Mock extraction failure
        mock_article = Mock()
        mock_article.download.side_effect = Exception("Download failed")
        mock_article_class.return_value = mock_article
        
        # Execute
        new_count = pipeline.fetch_and_store_feed(feed_id)
        
        # Verify: Article still added with summary only
        assert new_count == 1
        articles = models.get_articles_by_feed(feed_id)
        assert len(articles) == 1
        assert articles[0]['summary'] == "Test summary"
        assert articles[0]['full_text'] is None
