"""SQLite schema definitions and initialization."""

import sqlite3
from pathlib import Path


SCHEMA_VERSION = 1

SCHEMA_SQL = """
-- Feeds table
CREATE TABLE IF NOT EXISTS feeds (
    feed_id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Articles table
CREATE TABLE IF NOT EXISTS articles (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    feed_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL UNIQUE,
    summary TEXT,
    full_text TEXT,
    published_date TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (feed_id) REFERENCES feeds(feed_id) ON DELETE CASCADE
);

-- User likes table
CREATE TABLE IF NOT EXISTS user_likes (
    article_id INTEGER NOT NULL,
    user_id INTEGER DEFAULT 1,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (article_id, user_id),
    FOREIGN KEY (article_id) REFERENCES articles(article_id) ON DELETE CASCADE
);

-- Embeddings table for ML recommendations
CREATE TABLE IF NOT EXISTS embeddings (
    article_id INTEGER PRIMARY KEY,
    embedding BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (article_id) REFERENCES articles(article_id) ON DELETE CASCADE
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_articles_feed_id ON articles(feed_id);
CREATE INDEX IF NOT EXISTS idx_articles_published_date ON articles(published_date DESC);
CREATE INDEX IF NOT EXISTS idx_user_likes_article_id ON user_likes(article_id);
"""


def create_schema(conn: sqlite3.Connection) -> None:
    """Create database schema.
    
    Args:
        conn: SQLite database connection
    """
    conn.executescript(SCHEMA_SQL)
    conn.commit()


def initialize_database(db_path: str | Path = "rss_reader.db") -> sqlite3.Connection:
    """Initialize database with schema.
    
    Args:
        db_path: Path to SQLite database file
        
    Returns:
        Database connection
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    
    create_schema(conn)
    
    return conn
