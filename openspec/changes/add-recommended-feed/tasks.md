# Implementation Tasks

## 1. Feed List Widget
- [ ] 1.1 Add "Recommended" virtual feed item below "All Articles"
- [ ] 1.2 Use feed_id=-1 for recommendations
- [ ] 1.3 Style with distinct icon (e.g., ✨ or 🎯)
- [ ] 1.4 Calculate recommendation count (0 if < 5 liked articles)
- [ ] 1.5 Grey out or show disabled state when no recommendations available

## 2. Article List Widget
- [ ] 2.1 Detect when feed_id=-1 (Recommended feed)
- [ ] 2.2 Call get_recommendations() from ML module
- [ ] 2.3 Display articles with similarity scores (optional)
- [ ] 2.4 Show helpful message when < 5 articles liked
- [ ] 2.5 Handle ML module import errors gracefully

## 3. Recommendation Display
- [ ] 3.1 Sort articles by similarity score (highest first)
- [ ] 3.2 Show similarity percentage or score in article list (optional)
- [ ] 3.3 Include feed name prefix like "All Articles" view
- [ ] 3.4 Preserve liked indicator (♥) for already-liked articles
- [ ] 3.5 Limit to top 50 recommendations

## 4. UI Integration
- [ ] 4.1 Test selecting "Recommended" feed
- [ ] 4.2 Test navigation between Recommended and other feeds
- [ ] 4.3 Verify article reader works from recommendations
- [ ] 4.4 Test liking/unliking recommended articles
- [ ] 4.5 Decide: Keep or remove `r` keyboard shortcut

## 5. Empty State Handling
- [ ] 5.1 Show "Like 5+ articles to see recommendations" when insufficient data
- [ ] 5.2 Show count as "0" or "(none)" when no recommendations available
- [ ] 5.3 Update count after liking articles
- [ ] 5.4 Refresh recommendations when feed list refreshes

## 6. Testing & Validation
- [ ] 6.1 Test with < 5 liked articles (should show empty state)
- [ ] 6.2 Test with 5+ liked articles (should show recommendations)
- [ ] 6.3 Test liking articles updates recommendation count
- [ ] 6.4 Test recommendations update after feed refresh
- [ ] 6.5 Test ML module unavailable (graceful degradation)

## 7. Documentation
- [ ] 7.1 Update README to mention "Recommended" feed in sidebar
- [ ] 7.2 Update keyboard shortcuts if `r` key is removed
- [ ] 7.3 Add explanation of how to get recommendations
