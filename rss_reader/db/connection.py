"""SQLite connection management."""

import sqlite3
from pathlib import Path
from typing import Optional
import threading

from .schema import initialize_database


_connection: Optional[sqlite3.Connection] = None
_db_path: Path = Path("rss_reader.db")
_thread_local = threading.local()


def set_database_path(path: str | Path) -> None:
    """Set the database file path.
    
    Args:
        path: Path to SQLite database file
    """
    global _db_path
    _db_path = Path(path)


def get_connection() -> sqlite3.Connection:
    """Get or create database connection for current thread.
    
    Returns:
        SQLite connection with row factory enabled
    """
    # Use thread-local storage for connections
    if not hasattr(_thread_local, 'connection') or _thread_local.connection is None:
        _thread_local.connection = initialize_database(_db_path)
        _thread_local.connection.row_factory = sqlite3.Row
    
    return _thread_local.connection


def close_connection() -> None:
    """Close database connection for current thread."""
    if hasattr(_thread_local, 'connection') and _thread_local.connection is not None:
        _thread_local.connection.close()
        _thread_local.connection = None
