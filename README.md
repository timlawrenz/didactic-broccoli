# RSS Reader

A personalized RSS reader with ML-powered recommendations running in your terminal.

## Features

- Subscribe to RSS/Atom feeds
- Automatically fetch and extract full article text
- Store articles locally in SQLite database
- Like articles to build your preference profile
- **ML-powered recommendations** based on your reading preferences
- Interactive terminal UI with keyboard navigation

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

### Terminal UI (Recommended)

Launch the interactive TUI:

```bash
source .venv/bin/activate
rss-reader
```

**Browsing Articles:**
- The app starts with **"All Articles"** view showing posts from all feeds chronologically
- Click on "All Articles" or a specific feed name in the left sidebar to switch views
- In "All Articles" view, each article is prefixed with its feed name (e.g., "[Tech News] Article Title")
- Navigate with arrow keys or vim-style `j`/`k` keys

**Keyboard Shortcuts:**
- `q` - Quit application
- `u` - Update all feeds
- `l` - Like/unlike current article
- `a` - Add new feed
- `d` - Delete selected feed  
- `r` - Show personalized recommendations
- `j`/`k` - Navigate lists (vim-style)
- `↑`/`↓` - Navigate lists (arrow keys)
- `Tab` - Switch between panels
- `Enter` - Select item

### ML-Powered Recommendations

The RSS reader learns your preferences as you like articles and provides personalized recommendations:

1. **Like articles** (press `l`) that interest you
2. After liking **5 or more articles**, press `r` to see recommendations
3. The system uses:
   - **Sentence embeddings** (all-MiniLM-L6-v2 model) to understand article content
   - **K-Means clustering** to identify your diverse interests
   - **Cosine similarity** to find articles similar to your taste profile

**How it works:**
- Embeddings are generated automatically when fetching new articles
- Your liked articles are clustered into 5 taste profiles
- Recommendations are ranked by similarity to your interests
- Already-read articles are excluded

**Note:** The first time you update feeds, the sentence-transformers model (~80MB) will be downloaded automatically.

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
├── ml/              # ML embeddings and recommendations
└── ui/              # TUI interface with Textual
```

## Database Schema

The application uses SQLite with four main tables:

- **feeds**: Subscribed RSS feeds
- **articles**: Fetched articles with full text
- **user_likes**: User's liked articles
- **embeddings**: 384-dimensional article embeddings for ML

Database file: `rss_reader.db` (created automatically on first run)

## Roadmap

- [x] Phase 1: Foundation (Python structure, database, RSS fetching)
- [x] Phase 2: TUI interface with Textual
- [x] Phase 3: ML recommendations with embeddings

## License

TBD
