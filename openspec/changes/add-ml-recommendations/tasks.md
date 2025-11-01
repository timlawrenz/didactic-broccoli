# Implementation Tasks

## 1. Dependencies & Setup
- [ ] 1.1 Add sentence-transformers to dependencies
- [ ] 1.2 Add scikit-learn to dependencies
- [ ] 1.3 Research and add sqlite-vss or alternative vector search
- [ ] 1.4 Create `rss_reader/ml/` module structure

## 2. Database Schema Updates
- [ ] 2.1 Create embeddings table (article_id, embedding_vector)
- [ ] 2.2 Add database migration script
- [ ] 2.3 Create indexes for efficient vector lookup
- [ ] 2.4 Add helper methods to store/retrieve embeddings

## 3. Embedding Generation
- [ ] 3.1 Create `ml/embeddings.py` with sentence-transformers model
- [ ] 3.2 Implement text preprocessing (combine title + summary + full_text)
- [ ] 3.3 Add embedding generation function (all-MiniLM-L6-v2 model)
- [ ] 3.4 Integrate embedding generation into article fetch pipeline
- [ ] 3.5 Handle embedding failures gracefully (skip if model unavailable)

## 4. K-Means Clustering
- [ ] 4.1 Create `ml/clustering.py` with K-Means implementation
- [ ] 4.2 Implement function to get liked article embeddings
- [ ] 4.3 Implement centroid calculation from liked embeddings
- [ ] 4.4 Handle edge cases (< 5 liked articles)
- [ ] 4.5 Cache centroids for performance

## 5. Vector Search & Recommendations
- [ ] 5.1 Implement vector similarity search (sqlite-vss or fallback)
- [ ] 5.2 Create recommendation engine that combines clustering + search
- [ ] 5.3 Filter out already-read articles
- [ ] 5.4 Rank results by similarity score
- [ ] 5.5 Return top N recommendations (default 50)

## 6. TUI Integration
- [ ] 6.1 Create recommendations view/screen in TUI
- [ ] 6.2 Wire up `r` key to show recommendations
- [ ] 6.3 Display recommended articles with similarity scores
- [ ] 6.4 Handle "not enough liked articles" state
- [ ] 6.5 Add loading indicator during recommendation calculation

## 7. Testing & Validation
- [ ] 7.1 Unit tests for embedding generation
- [ ] 7.2 Unit tests for K-Means clustering
- [ ] 7.3 Integration test for full recommendation pipeline
- [ ] 7.4 Test with different numbers of liked articles (0, 1, 5, 100)
- [ ] 7.5 Verify performance (recommendations < 1 second)

## 8. Documentation & Polish
- [ ] 8.1 Update README with ML feature documentation
- [ ] 8.2 Add model download instructions
- [ ] 8.3 Document minimum liked articles threshold
- [ ] 8.4 Add example screenshots of recommendations
- [ ] 8.5 Create troubleshooting guide for ML issues
