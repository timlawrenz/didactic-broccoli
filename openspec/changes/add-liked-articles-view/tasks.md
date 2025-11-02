# Implementation Tasks

## 1. Feed List Widget
- [ ] 1.1 Add "Liked" virtual feed item below "Recommended"
- [ ] 1.2 Use feed_id=-2 for liked articles
- [ ] 1.3 Style with distinct icon (e.g., ♥ or 💖)
- [ ] 1.4 Calculate liked article count from database
- [ ] 1.5 Display count in sidebar (e.g., "♥ Liked (15)")

## 2. Article List Widget
- [ ] 2.1 Detect when feed_id=-2 (Liked feed)
- [ ] 2.2 Query get_liked_articles() from database
- [ ] 2.3 Sort articles by liked date (newest first)
- [ ] 2.4 Show feed name prefix for each article
- [ ] 2.5 Display all liked indicators (♥)

## 3. Display & Formatting
- [ ] 3.1 Include feed name prefix like "All Articles" view
- [ ] 3.2 Show published date for each article
- [ ] 3.3 Display liked indicator (♥) for all articles
- [ ] 3.4 Handle empty state (no liked articles yet)
- [ ] 3.5 Format consistently with other virtual feeds

## 4. Unlike Functionality
- [ ] 4.1 Test unliking articles from Liked view
- [ ] 4.2 Verify article disappears from list after unlike
- [ ] 4.3 Update count in sidebar after unlike
- [ ] 4.4 Refresh Recommended feed count if needed
- [ ] 4.5 Test rapid like/unlike toggling

## 5. UI Integration
- [ ] 5.1 Test selecting "Liked" feed
- [ ] 5.2 Test navigation between Liked and other feeds
- [ ] 5.3 Verify article reader works from Liked view
- [ ] 5.4 Test keyboard navigation (j/k)
- [ ] 5.5 Ensure Tab key switches panels correctly

## 6. Empty State Handling
- [ ] 6.1 Show "No liked articles yet" when empty
- [ ] 6.2 Add helpful message: "Press 'l' while reading to like articles"
- [ ] 6.3 Update count to show (0) when no likes
- [ ] 6.4 Handle user unliking last article

## 7. Testing & Validation
- [ ] 7.1 Test with 0 liked articles (empty state)
- [ ] 7.2 Test with 1 liked article
- [ ] 7.3 Test with many liked articles (50+)
- [ ] 7.4 Test unliking from Liked view
- [ ] 7.5 Test sorting (newest first)
- [ ] 7.6 Verify feed name prefixes display correctly
- [ ] 7.7 Test switching between feeds

## 8. Documentation
- [ ] 8.1 Update README to mention "Liked" feed
- [ ] 8.2 Explain how to view and manage liked articles
- [ ] 8.3 Add to feature list
