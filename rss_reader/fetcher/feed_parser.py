"""RSS feed fetching and parsing."""

import logging
from typing import Optional
from datetime import datetime

import feedparser
from feedparser import FeedParserDict


logger = logging.getLogger(__name__)


class FeedFetchError(Exception):
    """Error fetching or parsing RSS feed."""
    pass


def fetch_feed(url: str) -> FeedParserDict:
    """Fetch and parse RSS/Atom feed.
    
    Args:
        url: RSS feed URL
        
    Returns:
        Parsed feed data
        
    Raises:
        FeedFetchError: If feed cannot be fetched or parsed
    """
    try:
        feed = feedparser.parse(url)
        
        # Check for HTTP errors
        if hasattr(feed, 'status') and feed.status >= 400:
            raise FeedFetchError(f"HTTP {feed.status} error fetching feed: {url}")
        
        # Check if feed is valid
        if feed.bozo and not feed.entries:
            error = getattr(feed, 'bozo_exception', 'Unknown error')
            raise FeedFetchError(f"Invalid feed format: {error}")
        
        return feed
        
    except Exception as e:
        if isinstance(e, FeedFetchError):
            raise
        raise FeedFetchError(f"Error fetching feed {url}: {e}")


def parse_feed(feed: FeedParserDict) -> list[dict]:
    """Extract article data from parsed feed.
    
    Args:
        feed: Parsed feed data from feedparser
        
    Returns:
        List of article dictionaries with keys: title, link, summary, published_date
    """
    articles = []
    
    for entry in feed.entries:
        # Skip entries missing required fields
        if not hasattr(entry, 'title') or not hasattr(entry, 'link'):
            logger.warning(f"Skipping entry missing title or link: {entry.get('id', 'unknown')}")
            continue
        
        # Extract published date
        published_date = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                published_date = datetime(*entry.published_parsed[:6])
            except (TypeError, ValueError):
                pass
        
        article = {
            'title': entry.title,
            'link': entry.link,
            'summary': getattr(entry, 'summary', None),
            'published_date': published_date,
        }
        
        articles.append(article)
    
    logger.info(f"Parsed {len(articles)} articles from feed")
    return articles
