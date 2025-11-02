# Add Liked Articles View

## Why

Currently, users can like articles with `l` but there's no easy way to view all liked articles or unlike them. The only way to see liked articles is to remember which feed they came from and find them manually, which makes managing likes difficult. Users need a dedicated view to see all their liked articles in one place for easy review and management.

## What Changes

- Add a "Liked" virtual feed in the sidebar below "Recommended"
- Use feed_id=-2 for liked articles view
- Display all liked articles sorted by most recently liked (newest first)
- Show feed name prefix for each liked article (like "All Articles" view)
- Allow unliking articles directly from the Liked view (press `l`)
- Show article count in sidebar (number of liked articles)
- Include article metadata (date, feed name)

## Impact

- Affected specs: tui-interface (modified requirement)
- Affected code:
  - `rss_reader/ui/widgets/feed_list.py` - Add "Liked" feed item
  - `rss_reader/ui/widgets/article_list.py` - Handle feed_id=-2 for liked articles
- No breaking changes - purely additive
- Significantly improves like management UX
- Makes it easy to curate your liked collection

## Benefits

- **Easy review**: See all liked articles in one place
- **Simple management**: Unlike articles directly from the view
- **Clear visibility**: Count shows how many articles you've liked
- **Consistent pattern**: Follows "All Articles" and "Recommended" design
- **Better curation**: Manage your saved articles easily
