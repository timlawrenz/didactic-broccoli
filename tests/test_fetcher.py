"""Tests for RSS fetcher."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from rss_reader.fetcher import feed_parser, article_extractor


class TestFeedParser:
    """Test RSS feed parsing."""
    
    @patch('rss_reader.fetcher.feed_parser.feedparser.parse')
    def test_fetch_feed_success(self, mock_parse):
        """Test successful feed fetch."""
        mock_feed = Mock()
        mock_feed.status = 200
        mock_feed.entries = [Mock()]
        mock_feed.bozo = False
        mock_parse.return_value = mock_feed
        
        result = feed_parser.fetch_feed("https://example.com/feed")
        assert result == mock_feed
    
    @patch('rss_reader.fetcher.feed_parser.feedparser.parse')
    def test_fetch_feed_http_error(self, mock_parse):
        """Test feed fetch with HTTP error."""
        mock_feed = Mock()
        mock_feed.status = 404
        mock_feed.entries = []
        mock_parse.return_value = mock_feed
        
        with pytest.raises(feed_parser.FeedFetchError):
            feed_parser.fetch_feed("https://example.com/feed")
    
    @patch('rss_reader.fetcher.feed_parser.feedparser.parse')
    def test_fetch_feed_invalid_format(self, mock_parse):
        """Test feed fetch with invalid format."""
        mock_feed = Mock()
        mock_feed.bozo = True
        mock_feed.bozo_exception = "Invalid XML"
        mock_feed.entries = []
        mock_parse.return_value = mock_feed
        
        with pytest.raises(feed_parser.FeedFetchError):
            feed_parser.fetch_feed("https://example.com/feed")
    
    def test_parse_feed(self):
        """Test parsing feed entries."""
        mock_entry = Mock()
        mock_entry.title = "Test Article"
        mock_entry.link = "https://example.com/article"
        mock_entry.summary = "Test summary"
        mock_entry.published_parsed = (2024, 1, 1, 12, 0, 0, 0, 1, 0)
        
        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        
        articles = feed_parser.parse_feed(mock_feed)
        
        assert len(articles) == 1
        assert articles[0]['title'] == "Test Article"
        assert articles[0]['link'] == "https://example.com/article"
        assert articles[0]['summary'] == "Test summary"
        assert articles[0]['published_date'] == datetime(2024, 1, 1, 12, 0, 0)
    
    def test_parse_feed_skips_incomplete_entries(self):
        """Test parsing skips entries missing required fields."""
        mock_entry1 = Mock()
        mock_entry1.title = "Complete Article"
        mock_entry1.link = "https://example.com/complete"
        
        mock_entry2 = Mock(spec=['get'])  # No title or link
        mock_entry2.get.return_value = 'unknown'
        
        mock_feed = Mock()
        mock_feed.entries = [mock_entry1, mock_entry2]
        
        articles = feed_parser.parse_feed(mock_feed)
        
        assert len(articles) == 1
        assert articles[0]['title'] == "Complete Article"


class TestArticleExtractor:
    """Test article text extraction."""
    
    @patch('rss_reader.fetcher.article_extractor.Article')
    def test_extract_article_text_success(self, mock_article_class):
        """Test successful article extraction."""
        mock_article = Mock()
        mock_article.text = "Full article text content"
        mock_article_class.return_value = mock_article
        
        result = article_extractor.extract_article_text("https://example.com/article")
        
        assert result == "Full article text content"
        mock_article.download.assert_called_once()
        mock_article.parse.assert_called_once()
    
    @patch('rss_reader.fetcher.article_extractor.Article')
    def test_extract_article_text_failure(self, mock_article_class):
        """Test article extraction failure returns None."""
        mock_article = Mock()
        mock_article.download.side_effect = Exception("Download failed")
        mock_article_class.return_value = mock_article
        
        result = article_extractor.extract_article_text("https://example.com/article")
        
        assert result is None
    
    @patch('rss_reader.fetcher.article_extractor.Article')
    def test_extract_article_text_empty(self, mock_article_class):
        """Test article with no text returns None."""
        mock_article = Mock()
        mock_article.text = ""
        mock_article_class.return_value = mock_article
        
        result = article_extractor.extract_article_text("https://example.com/article")
        
        assert result is None
