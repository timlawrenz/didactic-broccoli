# Add ML-Powered Recommendations

## Why
Enable personalized article recommendations based on user preferences using CPU-based machine learning. When users like articles, the system learns their taste and recommends similar unread articles, creating a personalized reading experience without requiring GPU infrastructure.

## What Changes
- Add sentence-transformers for generating article embeddings (CPU-based)
- Add scikit-learn for K-Means clustering to find user taste profiles
- Add sqlite-vss extension for vector similarity search in SQLite
- Create ML module with embedding generation and recommendation engine
- Store article embeddings in database (new embeddings table)
- Wire up recommendations to the TUI's `r` key
- Generate embeddings when fetching new articles

## Impact
- Affected specs: ml-recommendations (new)
- Affected code: Creates `rss_reader/ml/` module, adds embeddings table to database
- Dependencies: Adds `sentence-transformers`, `scikit-learn`, `sqlite-vss`
- Database migration: Adds `embeddings` table with vector storage
- Performance: Embedding generation adds ~1-2s per article during fetch
