# Design: ML-Powered Recommendations

## Context
Implement a CPU-based machine learning recommendation system that learns user preferences from liked articles and suggests similar unread content. The system should be fast, simple, and work entirely offline without GPU requirements.

## Goals / Non-Goals

### Goals
- Generate meaningful recommendations based on liked articles
- Run efficiently on CPU-only systems
- Keep the entire system local (no cloud APIs)
- Provide fast recommendations (< 1 second after initial embedding)
- Scale to thousands of articles without performance issues

### Non-Goals
- GPU acceleration (must work on CPU)
- Real-time learning (batch processing is fine)
- Complex neural networks (keep models simple)
- Collaborative filtering (single-user system)
- Natural language generation (recommendations only)

## Decisions

### Decision: Use sentence-transformers with all-MiniLM-L6-v2
Use the `all-MiniLM-L6-v2` model from sentence-transformers library.

**Rationale:**
- Small model size (~80MB) downloads quickly
- Excellent performance on semantic similarity tasks
- Runs well on CPU (~50ms per article)
- Produces 384-dimensional embeddings (manageable size)
- Widely used and well-maintained

**Alternatives considered:**
- OpenAI embeddings: Requires API key and internet
- Larger BERT models: Too slow on CPU
- TF-IDF: Less semantic understanding
- Custom trained model: Too much complexity

### Decision: K-Means Clustering for Taste Profile
Use K-Means clustering (k=5) on liked article embeddings to find user taste centroids.

**Rationale:**
- Simple and interpretable algorithm
- Fast clustering (<100ms for hundreds of articles)
- Works well with 5 clusters to capture diverse interests
- Scikit-learn implementation is robust
- No training required

**Implementation:**
```python
from sklearn.cluster import KMeans

liked_embeddings = get_liked_embeddings()  # Shape: (n_articles, 384)
kmeans = KMeans(n_clusters=min(5, len(liked_embeddings)))
kmeans.fit(liked_embeddings)
centroids = kmeans.cluster_centers_  # Shape: (5, 384)
```

### Decision: SQLite with VSS Extension for Vector Search
Use `sqlite-vss` extension to add vector similarity search directly to SQLite.

**Rationale:**
- Keeps everything in one database file
- No need for separate index files
- Pure SQL queries for recommendations
- Fast enough for thousands of articles
- Easy to install and use

**Fallback:** If sqlite-vss is unavailable, use numpy cosine similarity (slower but works).

**Alternatives considered:**
- FAISS: Requires separate index file and more complexity
- Annoy: Another separate index, harder to sync with SQLite
- Pure numpy: Simpler but doesn't scale as well

### Decision: Embed Articles During Fetch
Generate embeddings when fetching new articles, not on-demand.

**Rationale:**
- Spreads computational cost over time
- Articles are immediately available for recommendations
- Avoids blocking user when they want recommendations
- Can retry failed embeddings later

**Trade-off:** Slightly slower article fetching, but more responsive recommendations.

### Decision: Minimum 5 Liked Articles for Recommendations
Require at least 5 liked articles before showing recommendations.

**Rationale:**
- K-Means needs multiple points to cluster meaningfully
- 5 articles is low enough to be achievable quickly
- Avoids poor recommendations from too little data
- Clear user feedback: "Like 5 articles to enable recommendations"

## Component Structure

```
rss_reader/ml/
├── __init__.py
├── embeddings.py       # Sentence-transformers model and embedding generation
├── clustering.py       # K-Means clustering for taste profiles
├── recommendations.py  # Main recommendation engine
└── vector_store.py     # Vector storage and similarity search
```

### Embeddings Module (embeddings.py)

**Purpose:** Generate semantic embeddings for article text.

**Key Functions:**
```python
def get_model() -> SentenceTransformer:
    """Load the embedding model (cached after first call)."""
    
def generate_embedding(text: str) -> np.ndarray:
    """Generate 384-dimensional embedding for text."""
    
def prepare_article_text(article: dict) -> str:
    """Combine title, summary, and full_text for embedding."""
```

**Model Loading:**
- Lazy load on first use
- Cache in module-level variable
- Handle import errors gracefully (if sentence-transformers not installed)

### Clustering Module (clustering.py)

**Purpose:** Find user taste profiles using K-Means clustering.

**Key Functions:**
```python
def get_taste_centroids(liked_article_ids: list[int]) -> np.ndarray:
    """Calculate K-Means centroids from liked articles.
    
    Returns:
        Array of shape (k, 384) representing taste centroids
    """
    
def calculate_clusters(embeddings: np.ndarray, k: int = 5) -> KMeans:
    """Run K-Means clustering on embeddings."""
```

**Edge Cases:**
- < 5 liked articles: Use k = len(liked_articles)
- No liked articles: Return None, show message
- All liked articles from one topic: Centroids will be close together (fine)

### Recommendations Module (recommendations.py)

**Purpose:** Main recommendation engine combining clustering and vector search.

**Key Functions:**
```python
def get_recommendations(user_id: int = 1, limit: int = 50) -> list[dict]:
    """Get personalized article recommendations.
    
    Returns:
        List of articles sorted by similarity score
    """
    
def score_article_similarity(article_embedding: np.ndarray, 
                            centroids: np.ndarray) -> float:
    """Calculate similarity score for an article against centroids."""
```

**Algorithm:**
1. Get liked article IDs for user
2. If < 5 liked articles, return empty with message
3. Calculate K-Means centroids from liked embeddings
4. Query vector store for articles similar to any centroid
5. Filter out already-liked and already-read articles
6. Rank by maximum similarity to any centroid
7. Return top N

### Vector Store Module (vector_store.py)

**Purpose:** Store and search article embeddings.

**Database Schema:**
```sql
CREATE TABLE embeddings (
    article_id INTEGER PRIMARY KEY,
    embedding BLOB,  -- Serialized numpy array
    FOREIGN KEY (article_id) REFERENCES articles(article_id) ON DELETE CASCADE
);

-- For sqlite-vss (if available):
CREATE VIRTUAL TABLE embedding_index USING vss(
    embedding(384)
);
```

**Key Functions:**
```python
def store_embedding(article_id: int, embedding: np.ndarray) -> None:
    """Store embedding for an article."""
    
def search_similar(query_embedding: np.ndarray, limit: int = 50) -> list[tuple]:
    """Find articles similar to query embedding.
    
    Returns:
        List of (article_id, similarity_score) tuples
    """
```

**Implementation Details:**
- Serialize embeddings as numpy arrays to BLOB
- Use cosine similarity for comparison
- If sqlite-vss available, use it; otherwise, fall back to numpy scan

## Data Flow

### Embedding Generation Flow
```
Article Fetched
    ↓
Prepare Text (title + summary + full_text)
    ↓
Generate Embedding (sentence-transformers)
    ↓
Store in Database (embeddings table)
```

### Recommendation Flow
```
User Presses 'r'
    ↓
Load Liked Articles (from user_likes)
    ↓
Get Liked Embeddings (from embeddings table)
    ↓
Calculate K-Means Centroids (scikit-learn)
    ↓
Vector Search for Similar Articles (sqlite-vss)
    ↓
Filter & Rank Results
    ↓
Display in TUI
```

## Performance Considerations

### Embedding Generation
- **Speed:** ~50ms per article on CPU
- **Batch Processing:** Can parallelize if needed
- **Memory:** Model uses ~200MB RAM (acceptable)

**Optimization:** Generate embeddings only once per article, cache in DB.

### K-Means Clustering
- **Speed:** <100ms for 100 articles
- **Memory:** Minimal (just embeddings array)

**Optimization:** Cache centroids until user likes a new article.

### Vector Search
- **SQLite-VSS:** ~10-50ms for 1000 articles
- **Numpy Fallback:** ~100-200ms for 1000 articles

**Optimization:** Limit search space to unread articles only.

### Overall Latency
- **First recommendation:** ~500ms (calculate centroids + search)
- **Subsequent:** <100ms if centroids cached
- **Target:** < 1 second

## Edge Cases

### Not Enough Liked Articles
**Scenario:** User has liked < 5 articles.

**Handling:**
- Show message: "Like at least 5 articles to get recommendations"
- Optionally show random recent articles as fallback

### No Embeddings Available
**Scenario:** Article fetched but embedding generation failed.

**Handling:**
- Skip article in recommendations
- Log warning
- Don't block other articles

### Model Not Installed
**Scenario:** sentence-transformers not available.

**Handling:**
- Show error message on first recommendation attempt
- Provide installation instructions
- Disable 'r' key or show helpful message

### All Articles Already Read
**Scenario:** User has read everything.

**Handling:**
- Show message: "No unread articles to recommend. Press 'u' to update feeds."

## Testing Strategy

### Unit Tests
```python
def test_embedding_generation():
    text = "AI makes breakthrough in quantum computing"
    embedding = generate_embedding(text)
    assert embedding.shape == (384,)
    assert np.linalg.norm(embedding) > 0

def test_clustering_with_few_articles():
    # Test with < 5 liked articles
    embeddings = np.random.randn(3, 384)
    centroids = calculate_clusters(embeddings, k=3)
    assert centroids.shape == (3, 384)
```

### Integration Tests
```python
def test_full_recommendation_pipeline():
    # Like 5 articles
    # Generate recommendations
    # Verify returned articles are different
    # Verify similarity scores are reasonable
```

### Performance Tests
```python
def test_recommendation_speed():
    # Measure time to generate recommendations
    assert recommendation_time < 1.0  # seconds
```

## Dependencies

**New:**
- `sentence-transformers>=2.2` - Embedding generation
- `scikit-learn>=1.3` - K-Means clustering
- `sqlite-vss` (optional) - Vector similarity search
- `numpy>=1.24` (already included via other deps)

**No changes:**
- Database layer (just add new table)
- Fetcher module (add embedding call)

## Migration Plan

### Database Migration
```python
def migrate_add_embeddings_table():
    """Add embeddings table to existing database."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            article_id INTEGER PRIMARY KEY,
            embedding BLOB,
            FOREIGN KEY (article_id) REFERENCES articles(article_id) 
                ON DELETE CASCADE
        )
    """)
```

### Backfill Embeddings
For existing articles without embeddings, run a one-time script:
```python
def backfill_embeddings():
    """Generate embeddings for existing articles."""
    articles = get_articles_without_embeddings()
    for article in articles:
        text = prepare_article_text(article)
        embedding = generate_embedding(text)
        store_embedding(article['article_id'], embedding)
```

## Risks / Trade-offs

### Risk: Model Download Size
**Issue:** First run downloads ~80MB model.

**Mitigation:**
- Show progress bar during download
- Provide offline installation instructions
- Cache model locally after download

### Risk: CPU Performance on Older Machines
**Issue:** Embedding generation might be slow on old CPUs.

**Mitigation:**
- Make embedding generation optional
- Add flag to disable ML features
- Provide performance tuning tips in docs

### Trade-off: Accuracy vs Speed
**Current:** Using smaller model (MiniLM) for speed.

**Future:** Could offer larger model option for better accuracy.

### Trade-off: Storage Space
**Impact:** 384 floats * 4 bytes = ~1.5KB per article.

**Acceptable:** 1000 articles = 1.5MB (negligible).

## Open Questions

- [ ] Should we support multiple clustering algorithms (DBSCAN, hierarchical)?
- [ ] Should recommendations include a "diversity" factor to avoid echo chamber?
- [ ] Should we track which recommendations users actually read?
- [ ] Should we allow users to adjust the number of clusters (k)?
