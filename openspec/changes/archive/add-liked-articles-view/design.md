# Design: Liked Articles Virtual Feed

## Context

Users can like articles by pressing `l` while reading, which stores them in the database for ML recommendations. However, there's currently no easy way to:
- View all liked articles in one place
- Review what you've liked
- Unlike articles without finding them in their original feed
- See how many articles you've liked total

The "Liked" virtual feed addresses this by providing a dedicated view for liked article management.

## Goals / Non-Goals

### Goals
- Provide easy access to all liked articles
- Allow unliking articles directly from the view
- Show liked article count in sidebar
- Consistent with other virtual feeds (All Articles, Recommended)
- Simple implementation using existing database queries

### Non-Goals
- Advanced filtering/sorting options (keep it simple)
- Liked article categories or tags
- Export liked articles
- Notes or comments on liked articles
- Syncing likes across devices

## Decisions

### Decision: Use feed_id=-2 for Liked Articles

Use feed_id=-2 to represent the liked articles virtual feed.

**Rationale:**
- Consistent with virtual feed pattern
- feed_id=0 → "All Articles"
- feed_id=-1 → "Recommended"
- feed_id=-2 → "Liked"
- Negative IDs clearly indicate virtual feeds
- Simple to detect in code

### Decision: Sort by Most Recently Liked (Newest First)

Display liked articles with most recently liked at the top.

**Rationale:**
- Users likely want to see recent likes first
- Easy to review what you just liked
- Natural for curating a collection
- Matches user mental model
- Simple database query: ORDER BY liked_date DESC

**Alternative considered:** Sort by published date
- Rejected: Less useful for reviewing recent activity
- Could add as future enhancement

### Decision: Place Below "Recommended" in Sidebar

Show "Liked" feed between "Recommended" and the separator line.

**Rationale:**
- Logical grouping of virtual feeds
- "All Articles" → everything
- "Recommended" → ML suggestions
- "Liked" → your collection
- All virtual feeds together before real feeds

**Sidebar layout:**
```
📰 All Articles (45)
✨ Recommended (12)
♥ Liked (15)
─────────────────
9to5google (25)
Ars Technica (20)
```

### Decision: Use ♥ Emoji for Liked Feed

Use the heart emoji (♥) to visually represent the Liked feed.

**Rationale:**
- Matches the liked indicator in articles
- Universally recognized symbol for "favorites"
- Consistent with existing UI (♥ Liked)
- Clear and recognizable
- Fits with other feed emojis (📰, ✨)

**Alternative considered:** 💖, 🔖
- Rejected: ♥ is simpler and more consistent

### Decision: Show Feed Name Prefixes

Include feed name prefix for each liked article, like "All Articles" view.

**Rationale:**
- Users want to know where articles came from
- Helps with context and discovery
- Consistent with "All Articles" pattern
- Easy to implement (already exists)
- No additional database queries needed

**Example:**
```
♥ 9to5google The latest AI breakthrough... 2024-11-02
♥ Ars Technica How neural networks work... 2024-11-01
♥ TechCrunch Cursor introduces model... 2024-10-31
```

### Decision: Allow Unliking from Liked View

Let users press `l` to unlike articles directly from the Liked view.

**Rationale:**
- Consistent interaction (l toggles like/unlike everywhere)
- No need for separate "remove" command
- Natural user expectation
- Article disappears from list after unlike
- Simple implementation (existing unlike logic)

**Behavior:**
1. User presses `l` on liked article
2. Article is unliked in database
3. Article disappears from Liked list
4. Count updates in sidebar
5. Recommended count may update (if < 5 likes now)

### Decision: Empty State with Helpful Message

Show clear message when no articles are liked yet.

**Rationale:**
- Helps new users understand the feature
- Encourages engagement (press `l` to like)
- Consistent with Recommended feed empty state
- Better UX than blank list

**Message:**
```
No liked articles yet

Press 'l' while reading articles to save them here.
Liked articles are used for personalized recommendations.
```

## Component Changes

### Feed List Widget (`feed_list.py`)

**Add Liked feed item:**
```python
def load_feeds(self):
    # ... existing code ...
    
    # Add "All Articles"
    all_articles_item = FeedItem(0, "All Articles", total_count, is_all_articles=True)
    items.append(all_articles_item)
    
    # Add "Recommended"  
    recommended_item = FeedItem(-1, "Recommended", rec_count, is_recommended=True)
    items.append(recommended_item)
    
    # Add "Liked" (NEW)
    liked_count = len(get_liked_articles())
    liked_item = FeedItem(-2, "Liked", liked_count, is_liked=True)
    items.append(liked_item)
    
    # Add separator
    items.append(Label("[dim]─────────────────[/dim]"))
    
    # ... rest of feeds ...
```

**Update FeedItem rendering:**
```python
class FeedItem(Static):
    def __init__(self, feed_id, feed_name, article_count, 
                 is_all_articles=False, is_recommended=False, is_liked=False):
        # ... existing code ...
        self.is_liked = is_liked
    
    def render(self):
        if self.is_all_articles:
            return f"[bold]📰 {self.feed_name}[/bold] [dim]({self.article_count})[/dim]"
        if self.is_recommended:
            if self.article_count == 0:
                return f"[bold dim]✨ {self.feed_name}[/bold dim] [dim](0)[/dim]"
            return f"[bold]✨ {self.feed_name}[/bold] [dim]({self.article_count})[/dim]"
        if self.is_liked:
            return f"[bold]♥ {self.feed_name}[/bold] [dim]({self.article_count})[/dim]"
        return f"{self.feed_name} [dim]({self.article_count})[/dim]"
```

### Article List Widget (`article_list.py`)

**Add Liked feed handling:**
```python
def load_articles(self, feed_id: int):
    # ... existing code ...
    
    if feed_id == 0:
        articles = get_all_articles_sorted(limit=100)
    elif feed_id == -1:
        # Recommended feed logic
        # ... existing code ...
    elif feed_id == -2:
        # Liked feed (NEW)
        liked_articles = get_liked_articles()
        if not liked_articles:
            listview.append(ListItem(Label(
                "[dim]No liked articles yet[/dim]\n\n"
                "[dim]Press 'l' while reading articles to save them here.[/dim]\n"
                "[dim]Liked articles are used for personalized recommendations.[/dim]"
            )))
            return
        
        # Sort by most recently liked (newest first)
        # Note: get_liked_articles() should return liked_date
        articles = sorted(liked_articles, 
                         key=lambda x: x.get('liked_date', ''), 
                         reverse=True)
    else:
        articles = get_articles_by_feed(feed_id, limit=100)
    
    # ... rest of display logic ...
```

**Display with feed names:**
```python
    # Add feed name prefix for "All Articles", "Recommended", and "Liked" views
    if (feed_id == 0 or feed_id == -1 or feed_id == -2) and 'feed_name' in article:
        title = f"[cyan]{article['feed_name']}[/cyan] {article['title']}"
    else:
        title = article['title']
```

### Database Query Enhancement

The `get_liked_articles()` query should include `liked_date`:

```python
def get_liked_articles():
    """Get all liked articles with feed information."""
    conn = get_db_connection()
    cursor = conn.execute("""
        SELECT 
            a.article_id,
            a.title,
            a.link,
            a.summary,
            a.full_text,
            a.published_date,
            f.name as feed_name,
            la.liked_date
        FROM articles a
        JOIN feeds f ON a.feed_id = f.feed_id
        JOIN liked_articles la ON a.article_id = la.article_id
        WHERE la.user_id = 1
        ORDER BY la.liked_date DESC
    """)
    articles = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return articles
```

## User Flows

### Flow 1: First-Time User (No Likes)
1. User opens app
2. Sees "♥ Liked (0)" in sidebar
3. Clicks "Liked"
4. Sees empty state message
5. Understands they need to like articles
6. Browses and likes some articles

### Flow 2: Regular User (Has Likes)
1. User opens app
2. Sees "♥ Liked (15)" with count
3. Clicks "Liked"
4. Sees list of 15 liked articles
5. Articles sorted newest first
6. Each shows feed name + title + date
7. All have ♥ indicator

### Flow 3: Managing Likes
1. User in "Liked" view
2. Selects an article
3. Reads it in reader panel
4. Decides to unlike
5. Presses `l`
6. Article disappears from list
7. Count updates to (14)

### Flow 4: Reviewing Recent Likes
1. User likes several articles in a session
2. Clicks "Liked" to review
3. Most recent likes at top
4. Easy to see what was just liked
5. Can unlike if added by mistake

## Edge Cases

### Empty Likes List
- **Scenario:** User unlikes their last article
- **Behavior:** Show empty state message
- **Count:** Updates to (0)
- **No errors**

### All Articles from Same Feed
- **Scenario:** All likes from one feed
- **Behavior:** Still show feed name prefix
- **Reason:** Consistency, clarity

### Article Deleted from Feed
- **Scenario:** Liked article's feed deleted
- **Behavior:** Still show in Liked view
- **Feed name:** Show original feed name (stored in liked_articles)
- **Rationale:** Preserve user's curated collection

### Unlike While in Different View
- **Scenario:** Unlike article from its feed, then check Liked view
- **Behavior:** Article gone from Liked view
- **Count:** Updated
- **Consistency:** Database change reflected everywhere

### Rapid Like/Unlike Toggling
- **Scenario:** User toggles like rapidly
- **Behavior:** Each toggle processed
- **UI:** Updates reflect final state
- **Performance:** No lag or errors

## Testing Strategy

### Unit Tests
```python
def test_load_liked_articles():
    """Test loading liked articles view."""
    # Like some articles
    like_article(1, 1)  # article_id=1, user_id=1
    like_article(2, 1)
    
    # Load liked view
    articles = get_liked_articles()
    
    assert len(articles) == 2
    assert articles[0]['article_id'] == 2  # Most recent first
    assert 'feed_name' in articles[0]
    assert 'liked_date' in articles[0]

def test_unlike_from_liked_view():
    """Test unliking from liked view."""
    like_article(1, 1)
    articles_before = get_liked_articles()
    assert len(articles_before) == 1
    
    unlike_article(1, 1)
    articles_after = get_liked_articles()
    assert len(articles_after) == 0
```

### Integration Tests
- Load liked view with 0 articles
- Load liked view with 10 articles
- Unlike article from liked view
- Verify sorting (newest first)
- Check feed name prefixes display

### Manual Testing
1. Like articles from different feeds
2. Check "Liked" view shows all
3. Verify sorting (newest first)
4. Unlike an article
5. Verify it disappears
6. Check count updates
7. Test empty state

## Performance Considerations

### Database Query
- `get_liked_articles()` is already optimized
- Includes JOIN for feed names
- Returns all liked articles (typically < 100)
- Fast query (< 10ms)

### UI Rendering
- Similar to "All Articles" view
- No additional complexity
- Virtualized list handles large counts
- Smooth scrolling

### Refresh Behavior
- Liked view updates when:
  - User likes/unlikes article
  - Feed list is refreshed (u key)
- No automatic polling needed
- Lazy loading sufficient

## Alternatives Considered

### Alternative: Separate "Manage Likes" Modal

Show liked articles in a modal dialog instead of sidebar.

**Rejected because:**
- Inconsistent with virtual feed pattern
- Requires extra key binding
- Less discoverable
- More complex UI
- Sidebar integration is simpler

### Alternative: Add to Article List Context Menu

Right-click menu with "View Liked Articles".

**Rejected because:**
- TUI doesn't use context menus
- Keyboard-first interface
- Virtual feed more discoverable
- Sidebar is the natural place

### Alternative: Sort by Published Date

Sort liked articles by when they were published, not when liked.

**Rejected because:**
- Less useful for reviewing recent activity
- Published date can be old
- Liked date more relevant for curation
- Could add as toggle in future

### Alternative: Use feed_id=None Instead of -2

Use special value None for virtual feeds.

**Rejected because:**
- Breaks integer pattern
- Harder to check in conditionals
- Negative IDs cleaner
- Consistent with existing pattern

## Risks / Trade-offs

### Risk: Large Number of Likes

**Risk:** User has 1000+ liked articles.

**Mitigation:**
- Limit display to 100 most recent
- Add "Load more" if needed later
- Database query is still fast
- UI virtualization handles it

### Risk: Liked Article Feed Deleted

**Risk:** Feed deleted after article liked.

**Mitigation:**
- Store feed name in liked_articles table
- Article remains in Liked view
- Feed name shown correctly
- No broken references

### Trade-off: Another Virtual Feed

Adding third virtual feed increases sidebar items.

**Acceptable because:**
- Clear user benefit
- Follows established pattern
- Not cluttered (only 3 virtual feeds)
- User can ignore if not using likes

## Open Questions

- [ ] Should we add date range filter for liked articles?
- [ ] Should we add "Unlike all" bulk action?
- [ ] Should we show liked date in article list?
- [ ] Should we add export liked articles feature?

## Sign-Off Criteria

- [ ] "Liked" feed appears in sidebar with count
- [ ] Selecting it shows all liked articles
- [ ] Articles sorted by most recently liked
- [ ] Feed name prefixes display correctly
- [ ] Unliking from Liked view works
- [ ] Count updates after unlike
- [ ] Empty state message shows when no likes
- [ ] All existing tests pass
- [ ] Navigation works smoothly
- [ ] README updated
