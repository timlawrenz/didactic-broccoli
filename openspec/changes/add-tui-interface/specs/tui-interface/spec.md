# TUI Interface Specification

## ADDED Requirements

### Requirement: Three-Panel Layout
The application SHALL display a three-panel layout with feeds sidebar, article list, and article reader.

#### Scenario: Application launch
- **WHEN** the application starts
- **THEN** the screen shows three panels: feed list (left 20%), article list (center 30%), article reader (right 50%)

#### Scenario: Panel responsiveness
- **WHEN** the terminal window is resized
- **THEN** all panels adjust proportionally while maintaining readability

### Requirement: Feed List Display
The system SHALL display subscribed feeds in a scrollable sidebar with selection support.

#### Scenario: Show all feeds
- **WHEN** feeds exist in the database
- **THEN** each feed is displayed with its name in the sidebar

#### Scenario: Feed selection
- **WHEN** a user navigates with arrow keys and presses Enter on a feed
- **THEN** the feed is highlighted and its articles load in the article list panel

#### Scenario: Empty feed list
- **WHEN** no feeds are subscribed
- **THEN** a welcome message is displayed with instructions to press 'a' to add a feed

### Requirement: Article List Display
The system SHALL display articles from the selected feed with metadata and liked indicators.

#### Scenario: Show feed articles
- **WHEN** a feed is selected
- **THEN** articles from that feed are displayed with title, date, and liked indicator (♥)

#### Scenario: Article selection
- **WHEN** a user navigates with arrow keys and selects an article
- **THEN** the article is highlighted and its full content loads in the reader panel

#### Scenario: No articles
- **WHEN** a selected feed has no articles
- **THEN** a message displays "No articles yet. Press 'u' to fetch."

### Requirement: Article Reader Display
The system SHALL display the full article content with metadata in a scrollable reader panel.

#### Scenario: Show article content
- **WHEN** an article is selected
- **THEN** the reader displays title, link, publication date, and full article text

#### Scenario: Long article scrolling
- **WHEN** article text exceeds panel height
- **THEN** the user can scroll up/down with arrow keys, page up/down, or vim-style ctrl+u/ctrl+d

#### Scenario: Liked article indicator
- **WHEN** viewing a liked article
- **THEN** a "♥ Liked" indicator is shown in the article metadata

### Requirement: Keyboard Navigation
The system SHALL support keyboard shortcuts for all major actions without requiring mouse input.

#### Scenario: Quit application
- **WHEN** the user presses 'q'
- **THEN** the application exits gracefully

#### Scenario: Update feeds
- **WHEN** the user presses 'u'
- **THEN** all feeds are updated in the background and UI shows loading indicator

#### Scenario: Like article
- **WHEN** the user presses 'l' while viewing an article
- **THEN** the article is liked/unliked and indicator updates immediately

#### Scenario: Panel navigation
- **WHEN** the user presses Tab or Shift+Tab
- **THEN** focus moves to the next/previous panel

#### Scenario: Vim-style navigation
- **WHEN** the user presses 'j' or 'k' in a list
- **THEN** selection moves down or up respectively (same as arrow keys)

#### Scenario: Add feed
- **WHEN** the user presses 'a'
- **THEN** an "Add Feed" dialog appears with URL and name input fields

#### Scenario: Delete feed
- **WHEN** the user presses 'd' with a feed selected
- **THEN** a confirmation dialog appears before deletion

### Requirement: Background Feed Updates
The system SHALL fetch feed updates in background threads without blocking the UI.

#### Scenario: Non-blocking update
- **WHEN** the user presses 'u' to update feeds
- **THEN** the UI remains responsive and shows a loading indicator

#### Scenario: Update notification
- **WHEN** feed updates complete
- **THEN** a notification shows "Added X new articles from Y feeds"

#### Scenario: Update failure handling
- **WHEN** a feed fails to update
- **THEN** an error notification is shown but other feeds continue updating

### Requirement: Feed Management
The system SHALL provide dialogs for adding and removing feeds.

#### Scenario: Add new feed
- **WHEN** the user submits the "Add Feed" dialog with valid URL and name
- **THEN** the feed is added to the database and appears in the feed list

#### Scenario: Add invalid feed
- **WHEN** the user submits an invalid URL
- **THEN** an error message is displayed and the dialog remains open for correction

#### Scenario: Delete feed confirmation
- **WHEN** the user confirms feed deletion
- **THEN** the feed and all its articles are removed from the database and UI

### Requirement: Status Bar
The system SHALL display a status bar showing available keyboard shortcuts.

#### Scenario: Key hints display
- **WHEN** the application is running
- **THEN** the status bar shows: "[q] Quit [u] Update [l] Like [a] Add [d] Delete [j/k] Navigate"

#### Scenario: Context-sensitive hints
- **WHEN** a modal dialog is open
- **THEN** the status bar shows relevant shortcuts for that dialog

### Requirement: Visual Feedback
The system SHALL provide immediate visual feedback for user actions.

#### Scenario: Like action feedback
- **WHEN** the user likes an article
- **THEN** the heart indicator (♥) appears immediately in both article list and reader

#### Scenario: Loading indicator
- **WHEN** a background operation is running
- **THEN** a loading spinner or progress message is visible

#### Scenario: Error notifications
- **WHEN** an error occurs (network failure, invalid input)
- **THEN** a notification appears with the error message for 5 seconds

### Requirement: Empty State Handling
The system SHALL display helpful messages when there is no data to show.

#### Scenario: No feeds welcome
- **WHEN** the application starts with no subscribed feeds
- **THEN** a welcome message explains how to add the first feed

#### Scenario: No articles message
- **WHEN** a feed has no articles
- **THEN** a message suggests pressing 'u' to fetch articles

#### Scenario: No article selected
- **WHEN** no article is selected in the reader
- **THEN** a placeholder message says "Select an article to read"
