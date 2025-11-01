# RSS Reader

A personalized RSS reader with ML-powered recommendations running in your terminal.

## Features

- Subscribe to RSS/Atom feeds
- Automatically fetch and extract full article text
- Store articles locally in SQLite database
- Like articles to build your preference profile
- *Coming soon:* ML-based article recommendations

## Installation

### Requirements

- Python 3.10 or higher

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd didactic-broccoli
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Install development dependencies (optional):
```bash
pip install -e ".[dev]"
```

## Usage

### Python API

```python
from rss_reader.db import add_feed, get_all_feeds
from rss_reader.fetcher import fetch_and_store_feed

# Add a feed
feed_id = add_feed("https://feeds.arstechnica.com/arstechnica/index", "Ars Technica")

# Fetch articles
new_articles = fetch_and_store_feed(feed_id)
print(f"Added {new_articles} new articles")

# Get all feeds
feeds = get_all_feeds()
for feed in feeds:
    print(f"{feed['name']}: {feed['url']}")
```

## Development

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=rss_reader --cov-report=html
```

## Project Structure

```
rss_reader/
├── db/              # Database layer (SQLite)
├── fetcher/         # RSS fetching and article extraction
├── ml/              # ML embeddings and recommendations (coming soon)
└── ui/              # TUI interface (coming soon)
```

## Database Schema

The application uses SQLite with three main tables:

- **feeds**: Subscribed RSS feeds
- **articles**: Fetched articles with full text
- **user_likes**: User's liked articles

Database file: `rss_reader.db` (created automatically on first run)

## Roadmap

- [x] Phase 1: Foundation (Python structure, database, RSS fetching)
- [ ] Phase 2: TUI interface with Textual
- [ ] Phase 3: ML recommendations with embeddings

## License

TBD
