"""Data access models for feeds, articles, and user interactions."""

import sqlite3
from datetime import datetime
from typing import Optional

from .connection import get_connection


# Feed operations

def add_feed(url: str, name: str) -> int:
    """Add a new RSS feed.
    
    Args:
        url: RSS feed URL
        name: Display name for the feed
        
    Returns:
        feed_id of created feed
        
    Raises:
        sqlite3.IntegrityError: If feed URL already exists
    """
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO feeds (url, name) VALUES (?, ?)",
        (url, name)
    )
    conn.commit()
    return cursor.lastrowid


def get_feed(feed_id: int) -> Optional[sqlite3.Row]:
    """Get feed by ID.
    
    Args:
        feed_id: Feed ID
        
    Returns:
        Feed row or None if not found
    """
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM feeds WHERE feed_id = ?",
        (feed_id,)
    )
    return cursor.fetchone()


def get_all_feeds() -> list[sqlite3.Row]:
    """Get all feeds.
    
    Returns:
        List of feed rows
    """
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM feeds ORDER BY name"
    )
    return cursor.fetchall()


def update_feed_timestamp(feed_id: int) -> None:
    """Update feed's last_updated timestamp.
    
    Args:
        feed_id: Feed ID
    """
    conn = get_connection()
    conn.execute(
        "UPDATE feeds SET last_updated = CURRENT_TIMESTAMP WHERE feed_id = ?",
        (feed_id,)
    )
    conn.commit()


def delete_feed(feed_id: int) -> None:
    """Delete a feed and all its articles.
    
    Args:
        feed_id: Feed ID
    """
    conn = get_connection()
    conn.execute("DELETE FROM feeds WHERE feed_id = ?", (feed_id,))
    conn.commit()


# Article operations

def add_article(
    feed_id: int,
    title: str,
    link: str,
    summary: Optional[str] = None,
    full_text: Optional[str] = None,
    published_date: Optional[datetime] = None
) -> Optional[int]:
    """Add a new article.
    
    Args:
        feed_id: Feed ID
        title: Article title
        link: Article URL (must be unique)
        summary: Article summary
        full_text: Full article text
        published_date: Publication date
        
    Returns:
        article_id of created article, or None if duplicate
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            INSERT INTO articles (feed_id, title, link, summary, full_text, published_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (feed_id, title, link, summary, full_text, published_date)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # Duplicate article (link already exists)
        return None


def get_article(article_id: int) -> Optional[sqlite3.Row]:
    """Get article by ID.
    
    Args:
        article_id: Article ID
        
    Returns:
        Article row or None if not found
    """
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM articles WHERE article_id = ?",
        (article_id,)
    )
    return cursor.fetchone()


def get_articles_by_feed(feed_id: int, limit: int = 100) -> list[sqlite3.Row]:
    """Get articles for a feed.
    
    Args:
        feed_id: Feed ID
        limit: Maximum number of articles to return
        
    Returns:
        List of article rows
    """
    conn = get_connection()
    cursor = conn.execute(
        """
        SELECT * FROM articles 
        WHERE feed_id = ? 
        ORDER BY published_date DESC 
        LIMIT ?
        """,
        (feed_id, limit)
    )
    return cursor.fetchall()


# User interaction operations

def like_article(article_id: int, user_id: int = 1) -> None:
    """Like an article.
    
    Args:
        article_id: Article ID
        user_id: User ID (defaults to 1)
    """
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO user_likes (article_id, user_id) VALUES (?, ?)",
            (article_id, user_id)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # Already liked
        pass


def unlike_article(article_id: int, user_id: int = 1) -> None:
    """Unlike an article.
    
    Args:
        article_id: Article ID
        user_id: User ID (defaults to 1)
    """
    conn = get_connection()
    conn.execute(
        "DELETE FROM user_likes WHERE article_id = ? AND user_id = ?",
        (article_id, user_id)
    )
    conn.commit()


def get_liked_articles(user_id: int = 1, limit: int = 100) -> list[sqlite3.Row]:
    """Get articles liked by user.
    
    Args:
        user_id: User ID (defaults to 1)
        limit: Maximum number of articles to return
        
    Returns:
        List of article rows
    """
    conn = get_connection()
    cursor = conn.execute(
        """
        SELECT a.* FROM articles a
        INNER JOIN user_likes ul ON a.article_id = ul.article_id
        WHERE ul.user_id = ?
        ORDER BY ul.liked_at DESC
        LIMIT ?
        """,
        (user_id, limit)
    )
    return cursor.fetchall()
