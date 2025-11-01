"""Pipeline to orchestrate feed fetching and article storage."""

import logging

from ..db import models, get_connection
from .feed_parser import fetch_feed, parse_feed, FeedFetchError
from .article_extractor import extract_article_text


logger = logging.getLogger(__name__)


def fetch_and_store_feed(feed_id: int) -> int:
    """Fetch RSS feed and store articles in database.
    
    Args:
        feed_id: Feed ID to fetch
        
    Returns:
        Number of new articles added
        
    Raises:
        FeedFetchError: If feed cannot be fetched
    """
    # Get feed details
    feed = models.get_feed(feed_id)
    if not feed:
        raise ValueError(f"Feed {feed_id} not found")
    
    url = feed['url']
    logger.info(f"Fetching feed: {url}")
    
    # Fetch and parse feed
    try:
        feed_data = fetch_feed(url)
        articles = parse_feed(feed_data)
    except FeedFetchError as e:
        logger.error(f"Failed to fetch feed {url}: {e}")
        raise
    
    # Process articles
    new_count = 0
    for article_data in articles:
        # Extract full text (graceful degradation if it fails)
        full_text = extract_article_text(article_data['link'])
        
        # Store article
        article_id = models.add_article(
            feed_id=feed_id,
            title=article_data['title'],
            link=article_data['link'],
            summary=article_data['summary'],
            full_text=full_text,
            published_date=article_data['published_date']
        )
        
        if article_id:
            new_count += 1
            logger.debug(f"Added article: {article_data['title']}")
        else:
            logger.debug(f"Skipped duplicate article: {article_data['title']}")
    
    # Update feed timestamp
    models.update_feed_timestamp(feed_id)
    
    logger.info(f"Added {new_count} new articles from {url}")
    return new_count
