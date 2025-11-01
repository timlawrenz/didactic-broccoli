# Design: TUI Interface

## Context
Build a terminal user interface using Textual (modern Python TUI framework) that provides an interactive experience for browsing RSS feeds, reading articles, and managing preferences. The UI should be keyboard-driven, responsive, and feel like a native terminal application.

## Goals / Non-Goals

### Goals
- Create intuitive three-panel layout (feeds | articles | reader)
- Implement smooth keyboard navigation without mouse dependency
- Keep UI responsive during feed updates using background workers
- Provide visual feedback for all actions (likes, updates, errors)
- Support terminal window resizing gracefully

### Non-Goals
- Mouse-only navigation (keyboard-first approach)
- Complex theming system (use Textual's default with minimal customization)
- Offline mode indicators (defer to future enhancement)
- Article bookmarking or tagging (keep simple for MVP)

## Decisions

### Decision: Use Textual Framework
Textual is a modern, actively-maintained TUI framework with excellent documentation.

**Rationale:**
- CSS-like styling system makes layout intuitive
- Built-in widgets (ListView, ScrollView, etc.)
- Reactive data binding simplifies state management
- Worker threads for background tasks (perfect for feed fetching)

**Alternatives considered:**
- `urwid`: Older, less intuitive API
- `rich` + custom loop: Lower-level, more code to maintain
- `blessed`: Too low-level for complex layouts

### Decision: Three-Panel Layout
Classic RSS reader layout with feeds on left, articles in center, reader on right.

```
┌─────────────┬──────────────────┬─────────────────────┐
│  Feeds      │  Articles        │  Article Reader     │
│             │                  │                     │
│ • Tech News │  Latest AI ...   │  Title: ...         │
│ • Science   │  Space Tech ...  │                     │
│ • Business  │  Market Update..│  [Full article text]│
│             │                  │                     │
└─────────────┴──────────────────┴─────────────────────┘
[q] Quit [u] Update [l] Like [a] Add Feed [d] Delete
```

**Rationale:**
- Familiar pattern from desktop RSS readers
- Allows simultaneous view of context (feed), options (articles), and content (reader)
- Textual's `Horizontal` container makes this trivial

### Decision: Keyboard-First Navigation
Primary interaction via keyboard shortcuts, not mouse clicks.

**Key Bindings:**
- `q`: Quit application
- `u`: Update all feeds
- `l`: Like/unlike current article
- `a`: Add new feed
- `d`: Delete selected feed
- `r`: Show recommendations (placeholder for Phase 3)
- `tab`/`shift+tab`: Switch focus between panels
- `↑`/`↓` or `k`/`j`: Navigate lists (vim-style)
- `enter`: Select item
- `page up`/`page down` or `ctrl+u`/`ctrl+d`: Scroll reader (vim-style)

**Rationale:**
- Terminal users expect keyboard efficiency
- Faster than mouse for power users
- Works over SSH without X11

### Decision: Background Workers for Feed Updates
Use Textual's `@work` decorator to run feed fetching in background threads.

**Rationale:**
- Prevents UI freeze during network operations
- Textual handles thread-safety for UI updates
- Can show progress/loading indicators
- Allows canceling long-running fetches

**Implementation:**
```python
@work(thread=True)
async def update_feeds(self):
    for feed in get_all_feeds():
        new_count = fetch_and_store_feed(feed['feed_id'])
        self.post_message(FeedUpdated(feed, new_count))
```

### Decision: Defer Recommendations UI to Phase 3
Add `r` key binding now but show "Coming soon" message.

**Rationale:**
- ML recommendation engine not yet built (Phase 3)
- Can implement basic UI structure now
- Easier to test recommendation view in isolation later

## Component Structure

```
rss_reader/ui/
├── __init__.py
├── app.py                  # Main App class, layout, key bindings
├── widgets/
│   ├── __init__.py
│   ├── feed_list.py       # Sidebar feed list widget
│   ├── article_list.py    # Center article list widget
│   ├── article_reader.py  # Right panel article reader
│   └── dialogs.py         # Add feed, confirm delete modals
└── styles.css             # Textual CSS for styling (optional)
```

### Main App (app.py)
- Entry point: `def main() -> None`
- Compose layout with three panels
- Bind global keyboard shortcuts
- Manage application state (current feed, current article)
- Coordinate data flow between widgets

### Feed List Widget (feed_list.py)
- Display feeds as selectable ListView
- Highlight selected feed
- Show feed name + article count
- Emit `FeedSelected` message when feed clicked

### Article List Widget (article_list.py)
- Display articles from selected feed
- Show: title, date, liked indicator (♥)
- Emit `ArticleSelected` message when article clicked
- Auto-refresh when feed updates

### Article Reader Widget (article_reader.py)
- Display article metadata (title, link, date, feed name)
- Show full_text with word wrapping
- Scrollable for long articles
- Show "♥ Liked" indicator if article is liked

### Dialogs (dialogs.py)
- `AddFeedDialog`: Input form for URL + name
- `ConfirmDeleteDialog`: Yes/No confirmation

## Data Flow

1. **App starts** → Load feeds from DB → Display in feed list
2. **User selects feed** → Query articles from DB → Display in article list
3. **User selects article** → Load article details → Display in reader
4. **User presses `l`** → Like/unlike article → Update DB → Refresh UI
5. **User presses `u`** → Start background worker → Fetch feeds → Update DB → Notify user

## Error Handling Strategy

### Network Errors
- Show notification: "Failed to fetch [feed name]: Network error"
- Continue updating other feeds (don't stop batch)
- Log error details for debugging

### Empty States
- **No feeds**: Show welcome message with instructions to press `a`
- **No articles**: Show "No articles yet. Press 'u' to fetch."
- **Feed fetch failed**: Show "0 articles" but don't remove feed

### Invalid Input
- **Add feed with invalid URL**: Show error modal, don't close dialog
- **Add duplicate feed**: Show "Feed already exists" notification

## Styling Approach

Use Textual's CSS-like system for minimal, clean styling:

```css
Screen {
    background: $background;
}

#feed-list {
    width: 20%;
    border: solid $accent;
}

#article-list {
    width: 30%;
    border: solid $accent;
}

#article-reader {
    width: 50%;
    border: solid $accent;
}

.liked {
    color: $error;  /* Red heart */
}
```

## Performance Considerations

### Large Article Lists
- Lazy loading: Only render visible articles
- Textual's ListView handles virtualization automatically
- Limit initial query to 100 articles per feed

### Long Article Text
- Textual's ScrollView handles large text efficiently
- No need for custom pagination

### Feed Update Responsiveness
- Background workers prevent blocking
- Update articles incrementally as each feed completes
- Show progress: "Updated 3/10 feeds..."

## Testing Strategy

### Manual Testing
- Run with sample feeds (tech news, blogs)
- Test all keyboard shortcuts
- Verify layout on different terminal sizes (80x24, 120x40)
- Test feed update with slow network (throttle connection)

### Automated Testing (Future)
- Textual supports headless testing with `pilot`
- Defer to future enhancement (not blocking MVP)

## Dependencies

**New:**
- `textual>=0.40` - TUI framework

**No changes to existing:**
- Database layer remains unchanged
- Fetcher module remains unchanged

## Risks / Trade-offs

### Risk: Textual API Changes
**Status:** Textual is pre-1.0, API could change.

**Mitigation:**
- Pin to minor version (0.40.x)
- Monitor release notes before upgrading
- Abstract Textual-specific code into widgets

### Risk: Terminal Compatibility
**Potential issues:** Older terminals may not support features.

**Mitigation:**
- Test on common terminals (iTerm2, Terminal.app, GNOME Terminal, Windows Terminal)
- Graceful degradation for unsupported features
- Document minimum requirements in README

### Trade-off: Keyboard-Only vs Mouse Support
**Current:** Keyboard-first, mouse support is bonus.

**Future:** Textual supports mouse out-of-the-box, but we prioritize keyboard shortcuts.

## Migration Plan

N/A - This is a new feature, no migration needed. Existing database and fetcher modules remain unchanged.

## Open Questions

- [ ] Should we add vim-style `j`/`k` navigation in addition to arrow keys?
- [ ] Should article reader support markdown rendering (for blogs that use markdown)?
- [ ] Should we show unread count per feed?
