# Implementation Tasks

## 1. Feed List Widget
- [x] 1.1 Add "Liked" virtual feed item below "Recommended"
- [x] 1.2 Use feed_id=-2 for liked articles
- [x] 1.3 Style with distinct icon (e.g., ♥ or 💖)
- [x] 1.4 Calculate liked article count from database
- [x] 1.5 Display count in sidebar (e.g., "♥ Liked (15)")

## 2. Article List Widget
- [x] 2.1 Detect when feed_id=-2 (Liked feed)
- [x] 2.2 Query get_liked_articles() from database
- [x] 2.3 Sort articles by liked date (newest first)
- [x] 2.4 Show feed name prefix for each article
- [x] 2.5 Display all liked indicators (♥)

## 3. Display & Formatting
- [x] 3.1 Include feed name prefix like "All Articles" view
- [x] 3.2 Show published date for each article
- [x] 3.3 Display liked indicator (♥) for all articles
- [x] 3.4 Handle empty state (no liked articles yet)
- [x] 3.5 Format consistently with other virtual feeds

## 4. Unlike Functionality
- [x] 4.1 Test unliking articles from Liked view
- [x] 4.2 Verify article disappears from list after unlike
- [x] 4.3 Update count in sidebar after unlike
- [x] 4.4 Refresh Recommended feed count if needed
- [x] 4.5 Test rapid like/unlike toggling

## 5. UI Integration
- [x] 5.1 Test selecting "Liked" feed
- [x] 5.2 Test navigation between Liked and other feeds
- [x] 5.3 Verify article reader works from Liked view
- [x] 5.4 Test keyboard navigation (j/k)
- [x] 5.5 Ensure Tab key switches panels correctly

## 6. Empty State Handling
- [x] 6.1 Show "No liked articles yet" when empty
- [x] 6.2 Add helpful message: "Press 'l' while reading to like articles"
- [x] 6.3 Update count to show (0) when no likes
- [x] 6.4 Handle user unliking last article

## 7. Testing & Validation
- [x] 7.1 Test with 0 liked articles (empty state)
- [x] 7.2 Test with 1 liked article
- [x] 7.3 Test with many liked articles (50+)
- [x] 7.4 Test unliking from Liked view
- [x] 7.5 Test sorting (newest first)
- [x] 7.6 Verify feed name prefixes display correctly
- [x] 7.7 Test switching between feeds

## 8. Documentation
- [x] 8.1 Update README to mention "Liked" feed
- [x] 8.2 Explain how to view and manage liked articles
- [x] 8.3 Add to feature list
