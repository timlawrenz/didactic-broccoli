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

4. Install optional dependencies:
```bash
# Development tools
pip install -e ".[dev]"

# Tavily API for enhanced article extraction (optional)
pip install -e ".[tavily]"
```

5. Configure Tavily API (optional):
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your Tavily API key
# Get a free API key from: https://tavily.com
TAVILY_API_KEY=tvly-your-api-key-here
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
- Below that is **"Recommended"** - your personalized ML-powered article suggestions
- Below that is **"Liked"** - all your liked articles in one place for easy management
- Click on any feed name in the left sidebar to switch views
- In "All Articles", "Recommended", and "Liked" views, each article is prefixed with its feed name
- Navigate with arrow keys or vim-style `j`/`k` keys

**Managing Liked Articles:**
- Press `l` while reading any article to like (or unlike) it
- Click **"Liked"** in the sidebar to see all your liked articles
- Articles are sorted by most recently liked (newest first)
- Press `l` again to unlike directly from the Liked view
- Liked articles are used for personalized recommendations

**Keyboard Shortcuts:**
- `q` - Quit application
- `u` - Update all feeds
- `l` - Like/unlike current article
- `a` - Add new feed
- `d` - Delete selected feed
- `j`/`k` - Navigate lists (vim-style)
- `↑`/`↓` - Navigate lists (arrow keys)
- `Tab` - Switch between panels
- `Enter` - Select item

### ML-Powered Recommendations

The RSS reader learns your preferences as you like articles and provides personalized recommendations:

1. **Like articles** (press `l`) that interest you
2. After liking **5 or more articles**, the **"Recommended"** feed in the sidebar will show available recommendations
3. Click on **"Recommended"** to browse personalized article suggestions
4. The system uses:
   - **Sentence embeddings** (all-MiniLM-L6-v2 model) to understand article content
   - **K-Means clustering** to identify your diverse interests
   - **Cosine similarity** to find articles similar to your taste profile

**How it works:**
- Embeddings are generated automatically when fetching new articles
- Your liked articles are clustered into 5 taste profiles
- Recommendations are ranked by similarity score (shown as percentages)
- Articles are sorted by relevance (highest match first)
- Already-liked articles are excluded from recommendations

**Note:** The first time you update feeds, the sentence-transformers model (~80MB) will be downloaded automatically.

### Enhanced Article Extraction with Tavily (Optional)

For improved article extraction quality, especially from modern websites with JavaScript or dynamic content, you can use the Tavily API:

**Setup:**
1. Get a free API key from [Tavily.com](https://tavily.com) (1000 requests/month free tier)
2. Install the Tavily package: `pip install -e ".[tavily]"`
3. Set your API key in `.env`: `TAVILY_API_KEY=tvly-your-key-here`

**How it works:**
- The system tries Tavily API first for article extraction
- Falls back to newspaper3k if Tavily fails or is unavailable
- Tavily handles modern websites, dynamic content, and some paywalls better
- Completely optional - the app works without Tavily using newspaper3k

**Benefits:**
- Higher extraction success rate on modern websites
- Better content quality and formatting
- Handles JavaScript-heavy sites
- No configuration needed if you don't want it

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
