# Implementation Tasks

## 1. Database Layer
- [x] 1.1 Add `get_all_articles_sorted()` function to `db/models.py`
- [x] 1.2 Include feed name in article results
- [x] 1.3 Add optional limit parameter for pagination
- [x] 1.4 Sort by published_date DESC (newest first)
- [x] 1.5 Add unit tests for new database function

## 2. Feed List Widget
- [x] 2.1 Add "All Articles" as first item in feed list
- [x] 2.2 Style "All Articles" distinctly (e.g., bold or icon)
- [x] 2.3 Show total article count across all feeds
- [x] 2.4 Emit FeedSelected with special feed_id (e.g., 0 or -1)
- [x] 2.5 Highlight "All Articles" when selected

## 3. Article List Widget
- [x] 3.1 Detect when "All Articles" feed is selected
- [x] 3.2 Call `get_all_articles_sorted()` instead of `get_articles_by_feed()`
- [x] 3.3 Display feed name prefix in article titles (e.g., "[Feed Name] Article Title")
- [x] 3.4 Preserve liked indicator (♥) in combined view
- [x] 3.5 Handle empty state (no articles across any feed)

## 4. UI Integration
- [x] 4.1 Ensure "All Articles" loads by default on app start
- [x] 4.2 Test navigation between "All Articles" and specific feeds
- [x] 4.3 Verify article reader works correctly from combined view
- [x] 4.4 Test like/unlike functionality in combined view
- [x] 4.5 Update status bar to show "All Feeds" or specific feed name

## 5. Testing & Polish
- [x] 5.1 Test with 0 feeds (should show empty state)
- [x] 5.2 Test with 1 feed (combined view should match single feed)
- [x] 5.3 Test with multiple feeds (verify chronological ordering)
- [x] 5.4 Test with articles from same timestamp (consistent ordering)
- [x] 5.5 Verify performance with 100+ articles

## 6. Documentation
- [x] 6.1 Update README with "All Articles" feature
- [x] 6.2 Add to keyboard shortcuts documentation (if navigation changes)
- [x] 6.3 Update TUI screenshot/description if needed
