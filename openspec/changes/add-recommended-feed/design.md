# Design: Recommended Articles Feed

## Context

The ML recommendation system is currently accessible only via the `r` keyboard shortcut, which shows recommendations in a modal or separate view. This makes the feature less discoverable and breaks the natural flow of browsing feeds. By adding "Recommended" as a virtual feed in the sidebar, we integrate recommendations into the primary navigation pattern.

## Goals / Non-Goals

### Goals
- Make recommendations easily discoverable in feed list
- Integrate recommendations into natural browsing flow
- Show recommendation availability at a glance (count)
- Maintain consistency with "All Articles" virtual feed pattern
- Provide clear feedback when recommendations unavailable

### Non-Goals
- Real-time recommendation updates (batch is fine)
- Collaborative filtering (single-user recommendations)
- Explanation of why articles were recommended
- Recommendation feedback mechanism (beyond like/unlike)
- Custom recommendation preferences

## Decisions

### Decision: Use feed_id=-1 for Recommendations

When "Recommended" is selected, emit `FeedSelected(feed_id=-1, feed_name="Recommended")`.

**Rationale:**
- feed_id=-1 is invalid for real feeds (auto-increment starts at 1)
- feed_id=0 already used for "All Articles"
- Consistent with virtual feed pattern
- Easy to check: `if feed_id == -1: load_recommendations()`
- No new message type needed

**Alternatives considered:**
- feed_id=-2: Less memorable
- String ID: Breaks type consistency
- Separate message type: Unnecessary complexity

### Decision: Position Below "All Articles"

Place "Recommended" as second item in feed list, right below "All Articles".

**Rationale:**
- Logical grouping: virtual feeds at top
- High visibility for discovery
- Consistent pattern: special feeds first, then actual feeds
- Separator can distinguish virtual from real feeds

**Layout:**
```
📰 All Articles (45)
✨ Recommended (12)
─────────────────
9to5google (25)
Ars Technica (20)
```

### Decision: Show Count Based on ML Availability

Display recommendation count, or show "0"/"(none)" when < 5 articles liked.

**Rationale:**
- Provides immediate feedback on feature availability
- Encourages users to like more articles
- Consistent with feed count pattern
- No computation overhead (check liked count first)

**Implementation:**
```python
liked_count = len(get_liked_articles())
if liked_count >= 5:
    recommendations = get_recommendations(limit=50)
    count = len(recommendations)
else:
    count = 0  # or show "(like 5+)" hint
```

### Decision: Keep `r` Key for Quick Access (Optional)

Maintain `r` keyboard shortcut as alternative access method.

**Rationale:**
- Power users may prefer keyboard shortcuts
- No harm in having multiple access methods
- Matches pattern of other shortcuts
- Can be deprecated later if unused

**Alternative:** Remove `r` key since recommendations now in feed list.

### Decision: Include Feed Names in Recommendations

Show feed name prefix for each recommended article, like "All Articles" view.

**Rationale:**
- Users want to know article source
- Consistency with "All Articles" behavior
- Helps users evaluate recommendations
- May guide future feed subscriptions

**Format:** `[cyan]{feed_name}[/cyan] {article_title}`

### Decision: Optionally Show Similarity Scores

Display similarity percentage next to articles (e.g., "95% match").

**Rationale:**
- Helps users understand recommendation confidence
- Provides transparency into ML system
- Users can learn what makes good recommendations
- Can be toggled off if clutters UI

**Format:** `[dim](95% match)[/dim]` at end of article line

**Decision:** Make this optional (Phase 2 enhancement).

## Component Changes

### Feed List Widget (`ui/widgets/feed_list.py`)

Add "Recommended" item after "All Articles":

```python
def load_feeds(self):
    feeds = get_all_feeds()
    
    # Calculate counts
    total_count = sum(get_article_count(f['feed_id']) for f in feeds)
    
    # Add virtual feeds
    items = []
    items.append(FeedItem(0, "All Articles", total_count, is_all_articles=True))
    
    # Add Recommended feed
    liked_count = len(get_liked_articles())
    if liked_count >= 5:
        recommendations = get_recommendations(limit=50)
        rec_count = len(recommendations)
    else:
        rec_count = 0
    
    items.append(FeedItem(-1, "Recommended", rec_count, is_recommended=True))
    
    # Separator
    items.append(Label("[dim]─────────────────[/dim]"))
    
    # Add real feeds...
```

**Styling:**
- Use ✨ emoji for recommendations
- Bold text like "All Articles"
- Grey out when rec_count == 0

### Article List Widget (`ui/widgets/article_list.py`)

Handle feed_id=-1:

```python
def load_articles(self, feed_id: int):
    self.current_feed_id = feed_id
    listview = self.query_one("#article-listview", ListView)
    listview.clear()
    
    if feed_id == 0:
        # All Articles
        articles = get_all_articles_sorted(limit=100)
    elif feed_id == -1:
        # Recommended
        liked_count = len(get_liked_articles())
        if liked_count < 5:
            listview.append(ListItem(Label(
                f"[dim]Like at least 5 articles to see recommendations (you have {liked_count})[/dim]"
            )))
            return
        
        articles = get_recommendations(limit=50)
        if not articles:
            listview.append(ListItem(Label("[dim]No recommendations available[/dim]")))
            return
    else:
        # Single feed
        articles = get_articles_by_feed(feed_id, limit=100)
    
    # Render articles...
```

### Optional: Similarity Score Display

```python
# In article list rendering
if feed_id == -1 and 'similarity_score' in article:
    score_pct = int(article['similarity_score'] * 100)
    score_str = f" [dim]({score_pct}% match)[/dim]"
else:
    score_str = ""

label = Label(f"{heart}{title}{date_str}{score_str}")
```

## User Experience Flow

### First-Time User (< 5 Likes)
1. Opens app, sees "All Articles" and "Recommended (0)"
2. Clicks "Recommended"
3. Sees message: "Like at least 5 articles to see recommendations (you have 0)"
4. Understands they need to like articles first
5. Starts browsing and liking articles

### Returning User (5+ Likes)
1. Opens app, sees "Recommended (12)" with count
2. Clicks "Recommended"
3. Sees personalized article suggestions sorted by relevance
4. Articles include feed names and dates
5. Can read, like, or switch to other feeds

### Power User
1. Uses `r` key to quickly jump to recommendations
2. Browses recommendations, likes interesting ones
3. Recommendations update on next feed refresh
4. Can navigate with keyboard between feeds

## Empty States

### Insufficient Liked Articles
```
Like at least 5 articles to see recommendations (you have 3)

Try browsing "All Articles" and liking content that interests you!
```

### No Recommendations Available
```
No recommendations available

This can happen if there aren't enough similar articles in your feeds.
Try adding more feeds or liking more articles.
```

### ML Module Error
```
Recommendations temporarily unavailable

Please try again later.
```

## Performance Considerations

### Recommendation Generation
- Already implemented and efficient (< 1 second)
- K-Means clustering + cosine similarity
- Cached in-memory if implemented

### Feed List Loading
- Recommendations count check: O(1) liked articles check
- Only generate recommendations when needed (lazy loading)
- No performance impact on feed list rendering

### Refresh Strategy
- Recommendations refresh when feed list refreshes
- No automatic refresh (user-initiated via `u` key)
- Acceptable staleness for recommendations

## Error Handling

### ML Module Unavailable
Show "Recommended (0)" and graceful message when selected.

### Database Errors
Fall back to empty recommendations with error message.

### Zero Recommendations
Show helpful message guiding users to like more articles.

## Testing Strategy

### Manual Testing
1. Fresh install → verify shows "Recommended (0)"
2. Like 3 articles → verify count stays 0
3. Like 5 articles → verify count updates
4. Select Recommended → verify shows articles
5. Like article from recommendations → verify works
6. Refresh feeds → verify recommendations update

### Edge Cases
- All recommendations already liked
- Only 5 liked articles (minimum)
- 100+ liked articles (many recommendations)
- Recommendations from deleted feeds
- ML model not trained yet

## Migration Plan

N/A - This is purely additive. Existing `r` key functionality can be kept or removed.

## Alternatives Considered

### Alternative: Recommendations Tab

Add tab interface: "Feeds" vs "Recommended"

**Rejected because:**
- More complex UI changes
- Doesn't fit three-panel layout
- Less discoverable than sidebar item
- Requires new navigation pattern

### Alternative: Recommendations Panel

Separate fourth panel for recommendations.

**Rejected because:**
- Limited terminal width
- Over-complicates layout
- Violates three-panel design
- Harder to implement

### Alternative: Inline Recommendations

Mix recommended articles into "All Articles" feed.

**Rejected because:**
- Confusing - unclear what's recommended
- Can't see recommendations separately
- Dilutes feed experience
- Hard to control recommendation ratio

### Alternative: Keep Only `r` Key

Don't add to feed list, only keyboard shortcut.

**Rejected because:**
- Poor discoverability
- Inconsistent with feed browsing pattern
- Hides valuable feature
- Not intuitive for new users

## Risks / Trade-offs

### Risk: Cluttering Feed List

**Mitigation:** Virtual feeds clearly separated with separator line. Only 2 virtual feeds (All, Recommended).

### Risk: Empty Recommendations Confusion

**Mitigation:** Clear messaging when < 5 likes or no recommendations. Count shows availability.

### Risk: Stale Recommendations

**Mitigation:** Recommendations refresh on feed update (`u` key). Acceptable for MVP.

### Trade-off: Screen Space

Adding "Recommended" takes one line in feed list.

**Acceptable because:** Valuable feature worth the space. Users can still see 10-15 feeds easily.

## Open Questions

- [ ] Should similarity scores be shown by default or optional?
- [ ] Keep or remove `r` keyboard shortcut?
- [ ] Show "(none)" vs "0" for unavailable recommendations?
- [ ] Emoji: ✨ (sparkles) vs 🎯 (target) vs 💡 (bulb)?

## Sign-Off Criteria

- [ ] "Recommended" appears in feed list below "All Articles"
- [ ] Shows count of available recommendations
- [ ] Displays "0" or helpful message when < 5 liked articles
- [ ] Articles load when selected (if available)
- [ ] Feed names shown in article list
- [ ] Like/unlike works from recommendations
- [ ] Recommendations refresh on feed update
- [ ] Graceful handling when ML unavailable
