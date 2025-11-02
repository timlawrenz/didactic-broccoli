# Add Word-Wrap to Article Reader

## Why

Currently, the article reader in the right panel displays long lines of text without wrapping, causing horizontal scrolling and making articles difficult to read. This creates a poor reading experience, especially for articles with long paragraphs or URLs that extend beyond the panel width.

## What Changes

- Enable word-wrapping in the article reader widget
- Replace Label widget with ScrollableContainer for proper text flow
- Ensure text wraps at panel boundaries without horizontal scrolling
- Preserve formatting for titles, links, and metadata
- Maintain vertical scrolling functionality for long articles

## Impact

- Affected specs: tui-interface (modified requirement)
- Affected code:
  - `rss_reader/ui/widgets/article_reader.py` - Replace Label with proper wrapping widget
- No breaking changes - only improves readability
- Significant UX improvement for reading long articles
