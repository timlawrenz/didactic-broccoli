## ADDED Requirements

### Requirement: Liked Articles Virtual Feed

The TUI SHALL provide a "Liked" virtual feed that displays all liked articles for easy review and management.

#### Scenario: Display Liked feed in sidebar
- **WHEN** the TUI loads the feed list
- **THEN** a "Liked" virtual feed SHALL be displayed below "Recommended"
- **AND** the "Liked" feed SHALL use feed_id=-2
- **AND** the "Liked" feed SHALL show a count of liked articles
- **AND** the "Liked" feed SHALL be styled distinctly with ♥ icon

#### Scenario: Show liked article count
- **WHEN** the feed list is rendered
- **THEN** the "Liked" feed SHALL display the total count of liked articles
- **AND** the count SHALL be retrieved from get_liked_articles()
- **AND** the count SHALL update when articles are liked or unliked

#### Scenario: Load liked articles
- **WHEN** the user selects the "Liked" feed
- **AND** liked articles exist
- **THEN** the article list SHALL display all liked articles
- **AND** articles SHALL be sorted by liked date (newest first)
- **AND** each article SHALL include the feed name prefix
- **AND** the liked indicator (♥) SHALL be shown for all articles

#### Scenario: Empty state when no likes
- **WHEN** the user selects the "Liked" feed
- **AND** no articles have been liked yet
- **THEN** a helpful message SHALL be displayed
- **AND** the message SHALL say "No liked articles yet"
- **AND** the message SHALL explain how to like articles (press 'l')
- **AND** the message SHALL mention likes are used for recommendations

#### Scenario: Unlike from Liked view
- **WHEN** the user is viewing the "Liked" feed
- **AND** the user presses 'l' on a liked article
- **THEN** the article SHALL be unliked in the database
- **AND** the article SHALL disappear from the Liked list
- **AND** the "Liked" feed count SHALL decrease by 1
- **AND** the "Recommended" feed count MAY update if likes drop below 5

#### Scenario: Feed name prefixes display
- **WHEN** articles are displayed in the "Liked" feed
- **THEN** each article SHALL show its original feed name as a prefix
- **AND** the feed name SHALL be styled in cyan color
- **AND** the format SHALL be "[Feed Name] Article Title"
- **AND** the prefix SHALL be consistent with "All Articles" view

#### Scenario: Sort by recently liked
- **WHEN** liked articles are loaded
- **THEN** articles SHALL be sorted by liked_date in descending order
- **AND** the most recently liked article SHALL appear first
- **AND** older liked articles SHALL appear below

#### Scenario: Navigate from Liked view
- **WHEN** the user selects an article from the "Liked" feed
- **THEN** the article reader SHALL display the full article
- **AND** the article SHALL be openable with its link
- **AND** the unlike functionality (l key) SHALL work correctly
- **WHEN** the user switches from "Liked" to another feed
- **THEN** the article list SHALL update to show that feed's articles

#### Scenario: Update count after unlike
- **WHEN** a user unlikes their last liked article
- **THEN** the "Liked" feed count SHALL update to (0)
- **AND** the empty state message SHALL be displayed
- **AND** no errors SHALL occur

#### Scenario: Liked feed with many articles
- **WHEN** the user has liked 50+ articles
- **THEN** all liked articles SHALL be displayed in the list
- **AND** the UI SHALL handle scrolling smoothly
- **AND** performance SHALL remain responsive

## MODIFIED Requirements

### Requirement: Feed List Display

The TUI SHALL display subscribed RSS feeds in the left sidebar, with virtual feeds at the top.

#### Scenario: Feed list rendering with all virtual feeds
- **WHEN** the TUI loads
- **THEN** "All Articles" SHALL be displayed at the top
- **AND** "Recommended" SHALL be displayed below "All Articles"
- **AND** "Liked" SHALL be displayed below "Recommended"
- **AND** a separator line SHALL be displayed below virtual feeds
- **AND** individual feeds SHALL be displayed below the separator
- **AND** each item SHALL show its name and article count

#### Scenario: Virtual feed styling
- **WHEN** virtual feeds are displayed
- **THEN** "All Articles" SHALL be styled with bold text and 📰 emoji
- **AND** "Recommended" SHALL be styled with bold text and ✨ emoji
- **AND** "Liked" SHALL be styled with bold text and ♥ emoji
- **AND** virtual feeds SHALL be visually distinct from regular feeds
