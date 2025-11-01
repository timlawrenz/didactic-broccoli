# Add Project Foundation

## Why
Establish the foundational infrastructure for the RSS reader application including project structure, dependency management, database schema, and basic RSS fetching capabilities. This creates the data layer and core functionality needed before building the TUI interface and ML recommendation engine.

## What Changes
- Set up Python project with `pyproject.toml` and proper package structure
- Define SQLite database schema for feeds, articles, and user interactions
- Implement database initialization and basic CRUD operations
- Create RSS feed fetcher with `feedparser` integration
- Add article text extraction with `newspaper3k`
- Establish testing infrastructure for core components

## Impact
- Affected specs: project-structure, database-layer, rss-fetcher (all new)
- Affected code: Creates foundational codebase structure
- Dependencies: Introduces core Python packages (feedparser, newspaper3k, sqlite3)
- No breaking changes (greenfield project)
