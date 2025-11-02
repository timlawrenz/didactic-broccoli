## ADDED Requirements

### Requirement: Recommended Articles Virtual Feed

The TUI SHALL provide a "Recommended" virtual feed that displays ML-powered article recommendations in the feed list.

#### Scenario: Display Recommended feed in sidebar
- **WHEN** the TUI loads the feed list
- **THEN** a "Recommended" virtual feed SHALL be displayed below "All Articles"
- **AND** the "Recommended" feed SHALL use feed_id=-1
- **AND** the "Recommended" feed SHALL show a count of available recommendations
- **AND** the "Recommended" feed SHALL be styled distinctly with an icon (e.g., ✨)

#### Scenario: Show recommendation count
- **WHEN** the user has liked 5 or more articles
- **THEN** the "Recommended" feed SHALL display the count of available recommendations
- **AND** recommendations SHALL be generated using the ML module
- **WHEN** the user has liked fewer than 5 articles
- **THEN** the "Recommended" feed SHALL display a count of 0 or "(none)"

#### Scenario: Load recommended articles
- **WHEN** the user selects the "Recommended" feed
- **AND** 5 or more articles have been liked
- **THEN** the article list SHALL display ML-recommended articles
- **AND** articles SHALL be sorted by similarity score (highest first)
- **AND** each article SHALL include the feed name prefix
- **AND** the liked indicator (♥) SHALL be shown for already-liked articles
- **AND** recommendations SHALL be limited to top 50 articles

#### Scenario: Insufficient liked articles
- **WHEN** the user selects the "Recommended" feed
- **AND** fewer than 5 articles have been liked
- **THEN** a helpful message SHALL be displayed
- **AND** the message SHALL indicate how many more articles need to be liked
- **AND** the message SHALL say "Like at least 5 articles to see recommendations (you have X)"

#### Scenario: No recommendations available
- **WHEN** the user selects the "Recommended" feed
- **AND** 5 or more articles have been liked
- **AND** the ML module returns no recommendations
- **THEN** a message SHALL be displayed: "No recommendations available"
- **AND** the message SHALL suggest adding more feeds or liking more articles

#### Scenario: Recommendation count updates
- **WHEN** the user likes or unlikes an article
- **AND** the liked article count crosses the 5-article threshold
- **THEN** the "Recommended" feed count SHALL update on next refresh
- **WHEN** the user updates feeds (presses `u`)
- **THEN** the "Recommended" feed count SHALL recalculate

#### Scenario: Navigate from recommendations
- **WHEN** the user selects an article from the "Recommended" feed
- **THEN** the article reader SHALL display the full article
- **AND** the article SHALL be openable with its link
- **AND** the like/unlike functionality SHALL work correctly
- **WHEN** the user switches from "Recommended" to another feed
- **THEN** the article list SHALL update to show that feed's articles

#### Scenario: Optional similarity scores
- **WHEN** the user views the "Recommended" feed
- **THEN** articles MAY display similarity scores or match percentages
- **AND** scores SHALL be formatted as "(XX% match)" in dim text
- **AND** scores SHALL not interfere with article title readability

#### Scenario: ML module graceful degradation
- **WHEN** the ML module is unavailable or throws an error
- **THEN** the "Recommended" feed SHALL still appear in the feed list
- **AND** the count SHALL show 0
- **AND** selecting it SHALL show "Recommendations temporarily unavailable"
- **AND** no application errors SHALL occur

## MODIFIED Requirements

### Requirement: Feed List Display

The TUI SHALL display subscribed RSS feeds in the left sidebar, with virtual feeds at the top.

#### Scenario: Feed list rendering with virtual feeds
- **WHEN** the TUI loads
- **THEN** "All Articles" SHALL be displayed at the top
- **AND** "Recommended" SHALL be displayed below "All Articles"
- **AND** a separator line SHALL be displayed below virtual feeds
- **AND** individual feeds SHALL be displayed below the separator
- **AND** each item SHALL show its name and article count

#### Scenario: Virtual feed styling
- **WHEN** virtual feeds are displayed
- **THEN** "All Articles" SHALL be styled with bold text and 📰 emoji
- **AND** "Recommended" SHALL be styled with bold text and ✨ emoji
- **AND** virtual feeds SHALL be visually distinct from regular feeds
