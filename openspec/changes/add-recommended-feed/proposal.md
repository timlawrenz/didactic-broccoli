# Add Recommended Articles Feed

## Why

Currently, users must press `r` to view ML recommendations in a separate modal, which interrupts the browsing flow. The recommendations feature is hidden and requires users to discover the keyboard shortcut. Adding a "Recommended" virtual feed in the sidebar makes recommendations more discoverable and accessible, integrating them into the natural browsing experience alongside "All Articles" and individual feeds.

## What Changes

- Add a "Recommended" virtual feed below "All Articles" in the feed list
- Use feed_id=-1 for the recommendations feed
- Display recommended articles sorted by similarity score when selected
- Show article count based on available recommendations (require 5+ liked articles)
- Grey out or show "0" count when < 5 articles are liked
- Remove or deprecate the `r` keyboard shortcut (recommendations now in feed list)
- Include similarity scores in article display (optional enhancement)

## Impact

- Affected specs: tui-interface (new requirement)
- Affected code:
  - `rss_reader/ui/widgets/feed_list.py` - Add "Recommended" feed item
  - `rss_reader/ui/widgets/article_list.py` - Handle feed_id=-1 for recommendations
  - `rss_reader/ui/app.py` - Remove/deprecate `r` key binding (optional)
- No breaking changes - purely additive
- Improves discoverability of ML recommendations feature
- Better integrates recommendations into browsing flow
