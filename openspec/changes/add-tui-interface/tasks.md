# Implementation Tasks

## 1. Setup & Dependencies
- [x] 1.1 Add textual dependency to pyproject.toml
- [x] 1.2 Create `rss_reader/ui/` module structure
- [x] 1.3 Create `__init__.py` and main app entry point

## 2. Core Application Layout
- [x] 2.1 Create `ui/app.py` with main Textual App class
- [x] 2.2 Implement three-panel layout using Textual containers
- [x] 2.3 Create sidebar widget for feed list
- [x] 2.4 Create main panel widget for article list
- [x] 2.5 Create reader panel widget for article content
- [x] 2.6 Add status bar footer with key hints

## 3. Feed Management
- [x] 3.1 Create feed list widget with selection handling
- [x] 3.2 Implement "Add Feed" modal dialog
- [x] 3.3 Implement "Remove Feed" confirmation dialog
- [x] 3.4 Add keyboard shortcut `a` for add feed
- [x] 3.5 Add keyboard shortcut `d` for delete feed

## 4. Article Browsing
- [x] 4.1 Create article list widget with scrolling
- [x] 4.2 Display article title, feed name, and publish date
- [x] 4.3 Implement article selection with arrow keys
- [x] 4.4 Add "liked" indicator (♥) in article list
- [x] 4.5 Auto-load articles when feed is selected

## 5. Article Reader
- [x] 5.1 Create article reader widget with text wrapping
- [x] 5.2 Display full article text with scrolling
- [x] 5.3 Show article metadata (title, link, date)
- [x] 5.4 Implement `l` key to like/unlike current article
- [x] 5.5 Add visual feedback for like action

## 6. Feed Updates
- [x] 6.1 Implement `u` key to update feeds
- [x] 6.2 Run feed fetching in background thread (using Textual workers)
- [x] 6.3 Show loading indicator during update
- [x] 6.4 Display notification with update results
- [x] 6.5 Refresh article list after update

## 7. Navigation & UX
- [x] 7.1 Implement keyboard shortcuts (q=quit, u=update, l=like, r=recommendations placeholder)
- [x] 7.2 Add vim keybindings (j/k for up/down, ctrl+u/ctrl+d for page scroll)
- [x] 7.3 Add focus handling between panels (tab/shift+tab)
- [x] 7.4 Implement smooth scrolling for long content
- [x] 7.5 Add color scheme and styling with Textual CSS
- [x] 7.6 Handle empty states (no feeds, no articles)

## 8. Testing & Polish
- [ ] 8.1 Test with various feed formats
- [ ] 8.2 Test with long articles and titles
- [ ] 8.3 Add error handling for feed fetch failures
- [ ] 8.4 Create demo mode with sample data
- [ ] 8.5 Update README with TUI usage instructions
