"""RSS fetching and article extraction."""

from .feed_parser import fetch_feed, parse_feed, FeedFetchError
from .article_extractor import extract_article_text
from .pipeline import fetch_and_store_feed

__all__ = [
    "fetch_feed",
    "parse_feed",
    "FeedFetchError",
    "extract_article_text",
    "fetch_and_store_feed",
]
