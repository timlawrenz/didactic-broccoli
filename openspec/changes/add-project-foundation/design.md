# Design: Project Foundation

## Context
This is a greenfield project establishing the foundational architecture for a local-first, CPU-based RSS reader with ML recommendations. The design prioritizes simplicity, minimal dependencies, and single-file database storage.

## Goals / Non-Goals

### Goals
- Establish Python package structure suitable for future Homebrew/pip distribution
- Create reliable SQLite schema that supports future embedding storage
- Implement robust RSS fetching with graceful error handling
- Maintain single-user, local-first architecture

### Non-Goals
- Multi-user support or authentication
- Web API or remote access
- Complex ORM frameworks (use raw SQLite)
- Asynchronous fetching (keep synchronous for simplicity)

## Decisions

### Decision: Use pyproject.toml (PEP 621)
Modern Python packaging standard, works with pip, setuptools, and Homebrew.

**Alternatives considered:**
- `setup.py`: Legacy approach, less declarative
- Poetry: Additional tooling overhead for this simple project

### Decision: SQLite without ORM
Use Python's built-in `sqlite3` module directly with raw SQL.

**Rationale:**
- Zero dependencies for database layer
- Full control over schema and queries
- Simpler debugging and testing
- Performance is excellent for single-user use case

**Alternatives considered:**
- SQLAlchemy: Overkill for this simple schema
- Peewee: Lighter ORM but still unnecessary abstraction

### Decision: Synchronous Fetching
Initial implementation uses synchronous RSS fetching.

**Rationale:**
- Simpler error handling and debugging
- Feed updates happen in background thread via Textual (future work)
- Typical use case: 10-50 feeds, acceptable wait time

**Future:** Can add async with `aiohttp` if needed.

### Decision: Store Full Article Text
Extract and store complete article text, not just summaries.

**Rationale:**
- Better embedding quality for ML recommendations
- Enables full-text search
- Storage is cheap (SQLite handles compression well)

**Trade-off:** Larger database size, but acceptable for <10k articles.

## Schema Design

### feeds table
```sql
CREATE TABLE feeds (
    feed_id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    last_updated TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### articles table
```sql
CREATE TABLE articles (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    feed_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    link TEXT NOT NULL UNIQUE,
    summary TEXT,
    full_text TEXT,
    published_date TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (feed_id) REFERENCES feeds(feed_id) ON DELETE CASCADE
)
```

### user_likes table
```sql
CREATE TABLE user_likes (
    article_id INTEGER NOT NULL,
    user_id INTEGER DEFAULT 1,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (article_id, user_id),
    FOREIGN KEY (article_id) REFERENCES articles(article_id) ON DELETE CASCADE
)
```

**Notes:**
- `user_id` defaults to 1 (single-user design)
- `link` is UNIQUE to prevent duplicate articles
- Foreign keys with CASCADE delete for data integrity
- Timestamps for future sorting/filtering features

## Directory Structure

```
rss_reader/
├── pyproject.toml           # Project metadata, dependencies
├── README.md                # Setup and usage instructions
├── rss_reader/              # Main package
│   ├── __init__.py
│   ├── db/                  # Database layer
│   │   ├── __init__.py
│   │   ├── schema.py        # Table definitions and initialization
│   │   ├── connection.py    # SQLite connection management
│   │   └── models.py        # CRUD operations
│   └── fetcher/             # RSS fetching
│       ├── __init__.py
│       ├── feed_parser.py   # feedparser wrapper
│       ├── article_extractor.py  # newspaper3k wrapper
│       └── pipeline.py      # Orchestration: fetch → parse → store
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_db.py
│   ├── test_fetcher.py
│   └── fixtures/            # Sample RSS feeds for testing
└── .gitignore
```

## Error Handling Strategy

### Network Errors
- Catch `URLError`, `HTTPError` from feedparser
- Log error and skip feed (don't crash app)
- Store error state in `feeds.last_error` (future enhancement)

### Malformed RSS
- feedparser is lenient, but validate required fields (title, link)
- Skip articles missing critical data
- Log warnings for debugging

### Article Extraction Failures
- newspaper3k may fail on paywalls, JavaScript-heavy sites
- Gracefully degrade: store summary only if full_text extraction fails
- Continue processing other articles

## Testing Strategy

### Unit Tests
- Database CRUD operations with in-memory SQLite (`:memory:`)
- Feed parsing with mock RSS XML
- Article extraction with mock HTML

### Integration Tests
- Full pipeline: fetch real RSS feed → store → retrieve
- Use public test feed (e.g., https://feeds.arstechnica.com/arstechnica/index)
- Verify data integrity after round-trip

## Dependencies

**Core:**
- Python 3.10+ (for modern type hints)
- sqlite3 (built-in)

**Data Fetching:**
- `feedparser` ~6.0 - RSS/Atom parsing
- `newspaper3k` ~0.2 - Article text extraction
- `requests` ~2.31 - HTTP client (dependency of newspaper3k)

**Testing:**
- `pytest` ~7.4 - Test framework
- `pytest-cov` - Coverage reporting

## Risks / Trade-offs

### Risk: newspaper3k maintenance
**Status:** Last release 2018, but still works well for common sites.

**Mitigation:**
- Monitor for Python 3.12+ compatibility issues
- Consider alternatives: `trafilatura`, `readability-lxml` if needed

### Risk: SQLite file corruption
**Unlikely but possible with improper shutdown.**

**Mitigation:**
- Use `connection.commit()` after writes
- Add `PRAGMA journal_mode=WAL` for better concurrency
- Document backup strategy in README

### Trade-off: Synchronous vs Async
**Current:** Synchronous fetching is simpler.

**Future:** If updating 50+ feeds becomes slow (>30s), consider async with `aiohttp` + `asyncio`.

## Migration Plan

N/A - This is the initial implementation. Future schema changes will use SQLite `ALTER TABLE` or migration scripts.

## Open Questions

- [ ] Should we add `articles.read_status` field now or later? (Defer to TUI phase)
- [ ] Should `user_likes` track "dislike" or just "like"? (Start with like-only)
- [ ] Rate limiting for feed fetching? (Not needed initially, most feeds allow frequent polling)
