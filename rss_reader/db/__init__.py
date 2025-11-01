"""Database layer for RSS reader."""

from .connection import get_connection, initialize_database
from .models import (
    add_feed,
    get_feed,
    get_all_feeds,
    delete_feed,
    add_article,
    get_article,
    get_articles_by_feed,
    like_article,
    unlike_article,
    get_liked_articles,
)

__all__ = [
    "get_connection",
    "initialize_database",
    "add_feed",
    "get_feed",
    "get_all_feeds",
    "delete_feed",
    "add_article",
    "get_article",
    "get_articles_by_feed",
    "like_article",
    "unlike_article",
    "get_liked_articles",
]
