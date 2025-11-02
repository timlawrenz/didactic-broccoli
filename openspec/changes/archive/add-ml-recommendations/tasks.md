# Implementation Tasks

## 1. Dependencies & Setup
- [x] 1.1 Add sentence-transformers to dependencies
- [x] 1.2 Add scikit-learn to dependencies
- [x] 1.3 Research and add sqlite-vss or alternative vector search
- [x] 1.4 Create `rss_reader/ml/` module structure

## 2. Database Schema Updates
- [x] 2.1 Create embeddings table (article_id, embedding_vector)
- [x] 2.2 Add database migration script
- [x] 2.3 Create indexes for efficient vector lookup
- [x] 2.4 Add helper methods to store/retrieve embeddings

## 3. Embedding Generation
- [x] 3.1 Create `ml/embeddings.py` with sentence-transformers model
- [x] 3.2 Implement text preprocessing (combine title + summary + full_text)
- [x] 3.3 Add embedding generation function (all-MiniLM-L6-v2 model)
- [x] 3.4 Integrate embedding generation into article fetch pipeline
- [x] 3.5 Handle embedding failures gracefully (skip if model unavailable)

## 4. K-Means Clustering
- [x] 4.1 Create `ml/clustering.py` with K-Means implementation
- [x] 4.2 Implement function to get liked article embeddings
- [x] 4.3 Implement centroid calculation from liked embeddings
- [x] 4.4 Handle edge cases (< 5 liked articles)
- [x] 4.5 Cache centroids for performance

## 5. Vector Search & Recommendations
- [x] 5.1 Implement vector similarity search (sqlite-vss or fallback)
- [x] 5.2 Create recommendation engine that combines clustering + search
- [x] 5.3 Filter out already-read articles
- [x] 5.4 Rank results by similarity score
- [x] 5.5 Return top N recommendations (default 50)

## 6. TUI Integration
- [x] 6.1 Create recommendations view/screen in TUI
- [x] 6.2 Wire up `r` key to show recommendations
- [x] 6.3 Display recommended articles with similarity scores
- [x] 6.4 Handle "not enough liked articles" state
- [x] 6.5 Add loading indicator during recommendation calculation

## 7. Testing & Validation
- [x] 7.1 Unit tests for embedding generation
- [x] 7.2 Unit tests for K-Means clustering
- [x] 7.3 Integration test for full recommendation pipeline
- [x] 7.4 Test with different numbers of liked articles (0, 1, 5, 100)
- [x] 7.5 Verify performance (recommendations < 1 second)

## 8. Documentation & Polish
- [x] 8.1 Update README with ML feature documentation
- [x] 8.2 Add model download instructions
- [x] 8.3 Document minimum liked articles threshold
- [x] 8.4 Add example screenshots of recommendations
- [x] 8.5 Create troubleshooting guide for ML issues
