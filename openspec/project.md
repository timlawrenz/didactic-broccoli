# Project Context

## Purpose
A personalized RSS reader that uses machine learning embeddings and clustering to learn your interests and recommend new content based on your "liked" articles.

## Tech Stack

### Core Application
- **Language**: Python 3.x
- **Architecture**: Single Python project with TUI, fetcher, and ML logic integrated
- **Database**: SQLite (`rss_reader.db` - single file database)

### User Interface
- **Framework**: [Textual](https://textual.textualize.io/) - Modern TUI library with mouse support and CSS-like styling
- **Components**:
  - Sidebar: Subscribed feeds list
  - Main panel: Article titles list
  - Reader view: Selected article's full text
  - Keybindings: `u` (update feeds), `l` (like article), `r` (recommendations), `q` (quit)

### Data Layer
- **SQLite Tables**:
  - `feeds`: feed_id, url, name
  - `articles`: article_id, feed_id, title, link, summary, full_text, published_date
  - `user_likes`: article_id, user_id (single-user: user_id = 1)

### ML Stack (CPU-based)
- **Embeddings**: `sentence-transformers` library
  - Model: `all-MiniLM-L6-v2` (~100MB, CPU-optimized)
  - Generates embeddings via `model.encode(article_text)`
- **Clustering**: `scikit-learn`
  - Algorithm: K-Means (n_clusters=5)
  - Extracts taste centroids from liked article embeddings
  - Real-time clustering in memory

### Vector Search (Choose One)
**Option A: sqlite-vss (Recommended)**
- Loadable SQLite extension for vector similarity search
- Stores embeddings in virtual table within `rss_reader.db`
- Pure SQL queries for recommendations
- Single-file database solution

**Option B: faiss-cpu**
- Facebook/Meta's CPU-optimized vector search
- Separate `index.faiss` file alongside database
- Fast nearest-neighbor search
- Hybrid approach: FAISS for vectors, SQLite for metadata

### Content Fetching
- **RSS Parsing**: `feedparser`
- **Article Extraction**: `newspaper3k` (full text extraction)

## Project Conventions

### Code Style
- Follow PEP 8 Python style guidelines
- Type hints where appropriate for better code clarity
- Docstrings for public functions and classes

### Architecture Patterns
- **Minimal & Local-First**: All data stored locally, no cloud dependencies
- **Single Binary Goal**: Package for easy installation via Homebrew, pip, etc.
- **Async Background Tasks**: Use Textual's threading for feed updates
- **Single-User Design**: Optimized for personal use (user_id = 1)

### Application Workflow
1. **Launch**: Run `python my_rss_app.py` to start TUI
2. **Update Feeds** (`u` key):
   - Background thread fetches RSS feeds (`feedparser`)
   - Extract full article text (`newspaper3k`)
   - Generate embeddings (`sentence-transformers`)
   - Store articles + embeddings in database
3. **Read & Like** (`l` key):
   - Browse articles in main panel
   - Like articles to add to `user_likes` table
4. **Get Recommendations** (`r` key):
   - Pull liked embeddings from database
   - Run K-Means clustering to extract taste centroids
   - Query vector search (sqlite-vss or FAISS) for 50 nearest unread articles
   - Display sorted by similarity score

### Performance Considerations
- All ML operations run on CPU (no GPU required)
- K-Means clustering is near-instantaneous in memory
- Vector search optimized for <10k articles initially
- Embeddings cached in database to avoid recomputation

### Git Workflow
- `main` branch for stable releases
- Feature branches for development (`feature/*`)
- Small, focused commits with clear messages

### Dependencies
**Core**:
- `textual` - TUI framework
- `sqlite3` - Built-in Python module

**Data & Fetching**:
- `feedparser` - RSS/Atom feed parsing
- `newspaper3k` - Article text extraction

**ML & Search**:
- `sentence-transformers` - Text embeddings
- `scikit-learn` - K-Means clustering
- `sqlite-vss` OR `faiss-cpu` - Vector similarity search

### File Structure
```
rss_reader/
├── my_rss_app.py          # Main entry point
├── rss_reader.db          # SQLite database
├── ui/                    # Textual UI components
├── fetcher/               # RSS & article fetching
├── ml/                    # Embeddings & clustering
└── db/                    # Database models & queries
```
