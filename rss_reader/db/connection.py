"""SQLite connection management."""

import sqlite3
from pathlib import Path
from typing import Optional

from .schema import initialize_database


_connection: Optional[sqlite3.Connection] = None
_db_path: Path = Path("rss_reader.db")


def set_database_path(path: str | Path) -> None:
    """Set the database file path.
    
    Args:
        path: Path to SQLite database file
    """
    global _db_path
    _db_path = Path(path)


def get_connection() -> sqlite3.Connection:
    """Get or create database connection.
    
    Returns:
        SQLite connection with row factory enabled
    """
    global _connection
    
    if _connection is None:
        _connection = initialize_database(_db_path)
        _connection.row_factory = sqlite3.Row
    
    return _connection


def close_connection() -> None:
    """Close database connection."""
    global _connection
    
    if _connection is not None:
        _connection.close()
        _connection = None
