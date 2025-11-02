# Implementation Tasks

## 1. Feed List Widget
- [x] 1.1 Add "Recommended" virtual feed item below "All Articles"
- [x] 1.2 Use feed_id=-1 for recommendations
- [x] 1.3 Style with distinct icon (e.g., ✨ or 🎯)
- [x] 1.4 Calculate recommendation count (0 if < 5 liked articles)
- [x] 1.5 Grey out or show disabled state when no recommendations available

## 2. Article List Widget
- [x] 2.1 Detect when feed_id=-1 (Recommended feed)
- [x] 2.2 Call get_recommendations() from ML module
- [x] 2.3 Display articles with similarity scores (optional)
- [x] 2.4 Show helpful message when < 5 articles liked
- [x] 2.5 Handle ML module import errors gracefully

## 3. Recommendation Display
- [x] 3.1 Sort articles by similarity score (highest first)
- [x] 3.2 Show similarity percentage or score in article list (optional)
- [x] 3.3 Include feed name prefix like "All Articles" view
- [x] 3.4 Preserve liked indicator (♥) for already-liked articles
- [x] 3.5 Limit to top 50 recommendations

## 4. UI Integration
- [x] 4.1 Test selecting "Recommended" feed
- [x] 4.2 Test navigation between Recommended and other feeds
- [x] 4.3 Verify article reader works from recommendations
- [x] 4.4 Test liking/unliking recommended articles
- [x] 4.5 Decide: Keep or remove `r` keyboard shortcut

## 5. Empty State Handling
- [x] 5.1 Show "Like 5+ articles to see recommendations" when insufficient data
- [x] 5.2 Show count as "0" or "(none)" when no recommendations available
- [x] 5.3 Update count after liking articles
- [x] 5.4 Refresh recommendations when feed list refreshes

## 6. Testing & Validation
- [x] 6.1 Test with < 5 liked articles (should show empty state)
- [x] 6.2 Test with 5+ liked articles (should show recommendations)
- [x] 6.3 Test liking articles updates recommendation count
- [x] 6.4 Test recommendations update after feed refresh
- [x] 6.5 Test ML module unavailable (graceful degradation)

## 7. Documentation
- [x] 7.1 Update README to mention "Recommended" feed in sidebar
- [x] 7.2 Update keyboard shortcuts if `r` key is removed
- [x] 7.3 Add explanation of how to get recommendations
