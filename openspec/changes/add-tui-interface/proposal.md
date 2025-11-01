# Add TUI Interface

## Why
Create a terminal-based user interface using Textual that allows users to interactively browse feeds, read articles, and like content. This transforms the RSS reader from a Python API into a usable application with keyboard-driven navigation and a modern terminal UI.

## What Changes
- Add Textual framework as a dependency
- Create main TUI application with three-panel layout (feeds sidebar, article list, reader view)
- Implement keyboard bindings: `u` (update feeds), `l` (like), `r` (recommendations view), `q` (quit)
- Add feed management screen (add/remove feeds)
- Create article reader with text wrapping and scrolling
- Implement background thread for feed updates to keep UI responsive
- Add status bar showing current mode and key hints

## Impact
- Affected specs: tui-interface (new)
- Affected code: Creates `rss_reader/ui/` module
- Dependencies: Adds `textual>=0.40` to pyproject.toml
- No breaking changes to existing database or fetcher modules
