# Design: Article Reader Word-Wrap

## Context

The article reader currently uses a simple Label widget that doesn't wrap text. Long lines extend beyond the panel width, requiring horizontal scrolling and making articles difficult to read. This is especially problematic for articles with long paragraphs, URLs, or code blocks.

## Goals / Non-Goals

### Goals
- Enable automatic word-wrapping at panel boundaries
- Eliminate horizontal scrolling
- Maintain vertical scrolling for long articles
- Preserve text formatting (bold, dim, colors)
- Keep existing keyboard navigation

### Non-Goals
- Rich text rendering (markdown, HTML)
- Custom font sizes or styles
- Image display
- Hyperlink clicking
- Text search within article

## Decisions

### Decision: Use Static Widget with CSS Word-Wrap

Replace the Label widget with a Static widget inside a VerticalScroll container, with CSS configured for word-wrapping.

**Rationale:**
- Textual's Static widget supports word-wrap via CSS
- VerticalScroll provides scrolling for long content
- No need for custom text-wrapping logic
- Preserves rich text markup
- Native Textual solution

**Implementation:**
```python
class ArticleReader(Static):
    def compose(self) -> ComposeResult:
        yield Label("📖 Reader", id="reader-header")
        yield VerticalScroll(
            Static(id="reader-content"),
            id="reader-container"
        )
```

**CSS:**
```css
#reader-content {
    width: 100%;
    height: auto;
    overflow-x: hidden;
    overflow-y: auto;
    text-align: left;
}
```

### Decision: Use Static.update() for Content Changes

Continue using the update() method to change article content.

**Rationale:**
- Consistent with current implementation
- Efficient for content updates
- No widget re-mounting needed
- Simple API

### Decision: Keep Rich Text Markup

Continue using Textual's rich text markup for formatting.

**Rationale:**
- Already working in current implementation
- Supports bold, dim, colors out of the box
- No additional dependencies
- Familiar syntax

## Component Changes

### ArticleReader Widget (`ui/widgets/article_reader.py`)

**Current structure:**
```python
Container(
    Label("content", id="reader-content"),
    id="reader-container"
)
```

**New structure:**
```python
VerticalScroll(
    Static("content", id="reader-content"),
    id="reader-container"
)
```

**CSS additions:**
```python
DEFAULT_CSS = """
ArticleReader {
    width: 100%;
    height: 100%;
}

#reader-container {
    width: 100%;
    height: 1fr;
    overflow-x: hidden;
    overflow-y: auto;
}

#reader-content {
    width: 100%;
    height: auto;
    padding: 1;
}
"""
```

## Text Wrapping Behavior

### Short Lines
Text that fits within panel width displays normally, no wrapping.

### Long Lines
Text that exceeds panel width wraps to next line at word boundaries.

### Long URLs
URLs longer than panel width will wrap. Alternative: truncate with "..." but this may break copy-paste.

### Code Blocks
If articles contain code, it will wrap. Not ideal but acceptable for MVP.

## Scrolling Behavior

### Vertical Scrolling
- Mouse wheel: scrolls content
- Arrow keys: scrolls content
- Ctrl+u/Ctrl+d: page up/down (vim-style)
- Page Up/Page Down: page scrolling

### No Horizontal Scrolling
- Disabled via CSS
- Text wraps instead of requiring horizontal scroll

## Error Handling

### Empty Content
Show "[dim]No content available[/dim]" as before.

### Very Long Words
Words longer than panel width will break at panel boundary (CSS word-break).

### Special Characters
Rich text markup handles special characters correctly.

## Testing Strategy

### Manual Testing
1. Load article with short paragraphs → verify displays normally
2. Load article with long paragraphs → verify wraps at panel edge
3. Resize terminal → verify content reflows
4. Scroll long article → verify smooth scrolling
5. Test on 80-column terminal → verify readable

### Edge Cases
- Article with 500+ character paragraph
- Article with long URL (100+ chars)
- Article with unicode characters
- Empty article
- Article with only title (no body)

## Performance Considerations

### Rendering
Static widget with word-wrap is efficient for typical article lengths (1-10k characters).

### Memory
No significant memory overhead compared to Label.

### Reflow
Textual handles reflow on terminal resize automatically.

## Migration Plan

N/A - This is a drop-in replacement with no data changes.

## Alternatives Considered

### Alternative: Custom Text Wrapping

Implement manual text-wrapping in Python.

**Rejected because:**
- More complex
- Reinventing the wheel
- Textual already handles this
- More bugs to fix

### Alternative: Fixed Line Width

Wrap text at fixed character count (e.g., 80 chars).

**Rejected because:**
- Not responsive to terminal width
- Wastes space on wide terminals
- Poor UX on narrow terminals

### Alternative: Multiple Label Widgets

Create a Label per paragraph.

**Rejected because:**
- Complex widget management
- Harder to update content
- No benefit over Static

## Risks / Trade-offs

### Risk: Long URLs Breaking Layout

**Mitigation:** CSS handles URL wrapping. If still problematic, add custom URL shortening.

### Risk: Performance with Very Long Articles

**Mitigation:** Static widget handles thousands of lines efficiently. Tested with newspaper3k extracted articles.

### Trade-off: Code Block Readability

Code in articles will wrap, which may look odd.

**Acceptable because:** Most RSS articles don't contain code. Can improve later if needed.

## Open Questions

- [ ] Should we truncate very long URLs (>100 chars)?
- [ ] Add max-height to prevent extremely long articles?

## Sign-Off Criteria

- [ ] No horizontal scrolling in reader panel
- [ ] Text wraps at panel boundaries
- [ ] Vertical scrolling works for long articles
- [ ] Formatting (bold, links, dates) preserved
- [ ] Works on 80-column terminal
- [ ] Performance acceptable with 10k char articles
