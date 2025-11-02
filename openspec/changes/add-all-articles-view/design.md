# Design: All Articles View

## Context

Modern RSS readers typically offer two browsing modes:
1. **Single feed view**: Shows articles from one feed
2. **Combined view**: Shows articles from all feeds in chronological order

Our current TUI only supports single feed view, forcing users to switch between feeds to see recent content. Adding a combined "All Articles" view improves the browsing experience.

## Goals / Non-Goals

### Goals
- Provide chronological view of all articles across feeds
- Maintain existing single-feed behavior
- Display feed name to identify article source
- Keep UI responsive with many articles
- Default to "All Articles" on app startup

### Non-Goals
- Filtering by date range (defer to future)
- Grouping articles by feed (not needed for MVP)
- Infinite scroll/pagination (load all articles for now)
- Read/unread status tracking (not in scope)

## Decisions

### Decision: Use feed_id = 0 for "All Articles"

When "All Articles" is selected, emit `FeedSelected(feed_id=0, feed_name="All Articles")`.

**Rationale:**
- feed_id=0 is invalid for real feeds (auto-increment starts at 1)
- Easy to check: `if feed_id == 0: load_all_articles()`
- Doesn't require new message type
- Consistent with existing architecture

**Alternatives considered:**
- feed_id=-1: Less intuitive
- Null/None: Requires nullable handling
- New message type: Unnecessary complexity

### Decision: Prefix Article Titles with Feed Name

In combined view, show: `[Feed Name] Article Title`

**Rationale:**
- Users need to know article source
- Inline prefix avoids adding extra column
- Common pattern in RSS readers
- Works with existing article list widget

**Implementation:**
```python
if feed_id == 0:
    display_title = f"[{article['feed_name']}] {article['title']}"
else:
    display_title = article['title']
```

### Decision: Sort by Published Date DESC (Newest First)

Articles sorted from newest to oldest across all feeds.

**Rationale:**
- Users typically want most recent content first
- Matches expectations from other RSS readers
- Simple to implement with ORDER BY
- Predictable behavior

**Edge case:** Articles with same timestamp sorted by feed name, then title (deterministic).

### Decision: Load All Articles (No Pagination for MVP)

Query all articles across all feeds without pagination.

**Rationale:**
- Simplifies implementation
- Textual's ListView handles large lists efficiently (virtualization)
- Most users won't have thousands of articles
- Can add pagination later if needed

**Performance threshold:** If > 1000 articles, consider pagination.

### Decision: "All Articles" as Default View

App starts with "All Articles" selected by default.

**Rationale:**
- Better onboarding (show content immediately)
- Reduces clicks to see content
- Matches modern RSS reader UX
- Users can still select specific feeds

## Component Changes

### Database Layer (`db/models.py`)

Add new function:
```python
def get_all_articles_sorted(limit: Optional[int] = None) -> List[Dict]:
    """Get all articles from all feeds, sorted by published date (newest first).
    
    Returns:
        List of article dicts with feed_name included
    """
    conn = get_connection()
    query = """
        SELECT 
            a.article_id,
            a.title,
            a.link,
            a.summary,
            a.published_date,
            f.name as feed_name,
            f.feed_id
        FROM articles a
        JOIN feeds f ON a.feed_id = f.feed_id
        ORDER BY a.published_date DESC, f.name ASC, a.title ASC
    """
    if limit:
        query += f" LIMIT {limit}"
    
    cursor = conn.execute(query)
    return [dict(row) for row in cursor.fetchall()]
```

### Feed List Widget (`ui/widgets/feed_list.py`)

Changes:
1. Add "All Articles" as first feed item
2. Calculate total article count
3. Highlight when selected

```python
def load_feeds(self):
    feeds = get_all_feeds()
    
    # Add "All Articles" virtual feed
    total_articles = sum(self._get_article_count(f['feed_id']) for f in feeds)
    self.add_feed_item(0, "📰 All Articles", total_articles)
    
    # Add regular feeds
    for feed in feeds:
        count = self._get_article_count(feed['feed_id'])
        self.add_feed_item(feed['feed_id'], feed['name'], count)
```

### Article List Widget (`ui/widgets/article_list.py`)

Changes:
1. Check for feed_id == 0
2. Load articles from all feeds
3. Prefix titles with feed name

```python
def load_articles(self, feed_id: int):
    self.current_feed_id = feed_id
    
    if feed_id == 0:
        # Load all articles
        articles = get_all_articles_sorted()
        # Prefix with feed name
        for article in articles:
            article['display_title'] = f"[{article['feed_name']}] {article['title']}"
    else:
        # Load single feed
        articles = get_articles_by_feed(feed_id)
        for article in articles:
            article['display_title'] = article['title']
    
    self.render_articles(articles)
```

## UI Layout

No changes to three-panel layout. "All Articles" appears as first feed:

```
┌─────────────┬──────────────────┬─────────────────────┐
│  📰 All (45)│  Recent Articles │  Article Reader     │
│ ───────────│                  │                     │
│  Tech (25)  │ [Tech] Latest AI │  [Article content]  │
│  News (20)  │ [News] Markets...│                     │
│             │ [Tech] Python ...│                     │
└─────────────┴──────────────────┴─────────────────────┘
```

## Error Handling

### Empty States

- **No feeds**: Show "No feeds. Press 'a' to add one."
- **No articles**: Show "No articles yet. Press 'u' to fetch."
- **Feed deleted while viewing**: Gracefully return to "All Articles"

### Performance

- If query takes > 1 second, show loading indicator
- If > 1000 articles, log warning and suggest pagination

## Testing Strategy

### Unit Tests
- Test `get_all_articles_sorted()` with 0, 1, 10 feeds
- Verify chronological ordering
- Test with duplicate timestamps

### Manual Testing
- Navigate between "All Articles" and specific feeds
- Verify feed name prefixes appear/disappear correctly
- Test liking articles in combined view
- Verify article reader opens correct article

## Migration Plan

N/A - This is a purely additive feature. No data migration needed.

## Performance Considerations

### Expected Scale
- Typical user: 5-10 feeds, 50-200 articles
- Power user: 20+ feeds, 500+ articles
- Textual ListView: Handles thousands with virtualization

### Query Optimization
- JOIN on indexed feed_id is fast
- ORDER BY on published_date (already indexed)
- No N+1 queries (single query for all articles)

### Future Optimizations (if needed)
- Add pagination (LIMIT/OFFSET)
- Cache article counts
- Incremental loading (load more on scroll)

## Open Questions

- [ ] Should "All Articles" be bold/highlighted to distinguish from feeds?
- [ ] Show emoji icon (📰) or text only?
- [ ] Total count in "All Articles" or just show "All"?

## Alternatives Considered

### Alternative: Separate "All" button

Add button above feed list instead of treating as feed item.

**Rejected because:**
- Requires new UI component
- Less consistent with feed selection pattern
- More complex interaction model

### Alternative: Tabbed interface

Add tabs for "By Feed" vs "Combined" view.

**Rejected because:**
- Over-engineered for simple feature
- Doesn't fit current three-panel layout
- More navigation overhead

### Alternative: Filter button in article list

Add dropdown in article panel to switch between feeds.

**Rejected because:**
- Less discoverable
- Doesn't match RSS reader conventions
- Feed sidebar is natural place for this

## Risks / Trade-offs

### Risk: Performance with Many Articles

**Mitigation:** Test with 500+ articles. Add pagination if slow.

### Risk: Confusing Feed Name Prefixes

**Mitigation:** Use consistent format `[Feed] Title`. Keep feed name short.

### Trade-off: Screen Space for Feed Names

Prefixes use ~15-20 characters, leaving less for article title.

**Acceptable because:** Users need source context more than full title.

## Sign-Off Criteria

- [ ] "All Articles" appears at top of feed list
- [ ] Articles sorted chronologically (newest first)
- [ ] Feed names shown in combined view
- [ ] Performance acceptable with 100+ articles
- [ ] All existing functionality still works
