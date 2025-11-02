# Add "All Articles" View

## Why

Currently, users must select a specific feed to view its articles, which requires clicking through multiple feeds to see content. This creates friction when users want to browse all recent content across all subscriptions in a single chronological view, similar to how modern RSS readers like Feedly or Inoreader work.

## What Changes

- Add an "All Articles" virtual feed option at the top of the feed list
- Display combined articles from all feeds sorted by publish date (newest first)
- Show feed name alongside each article in the combined view
- Preserve existing single-feed behavior when a specific feed is selected
- Update database queries to efficiently fetch articles across all feeds

## Impact

- Affected specs: tui-interface (new requirement)
- Affected code: 
  - `rss_reader/ui/widgets/feed_list.py` - Add "All Articles" option
  - `rss_reader/ui/widgets/article_list.py` - Handle all-feeds mode
  - `rss_reader/db/models.py` - Add query for all articles sorted by date
- No breaking changes - existing behavior preserved
- Improved UX for browsing multiple feeds
