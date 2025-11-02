## ADDED Requirements

### Requirement: All Articles Combined View

The TUI SHALL provide a combined view showing articles from all RSS feeds in chronological order.

#### Scenario: User selects "All Articles"
- **WHEN** the user starts the TUI application
- **THEN** the "All Articles" option SHALL be displayed as the first item in the feed list
- **AND** the "All Articles" option SHALL show the total count of articles across all feeds
- **AND** the "All Articles" option SHALL be selected by default

#### Scenario: View articles from all feeds
- **WHEN** the user selects "All Articles" from the feed list
- **THEN** the article list SHALL display articles from all feeds
- **AND** articles SHALL be sorted by published date in descending order (newest first)
- **AND** each article SHALL be prefixed with its feed name in the format "[Feed Name] Article Title"
- **AND** the liked indicator (♥) SHALL be displayed for liked articles

#### Scenario: Navigate between combined and single feed view
- **WHEN** the user switches from "All Articles" to a specific feed
- **THEN** the article list SHALL display only articles from that feed
- **AND** article titles SHALL NOT be prefixed with feed names
- **WHEN** the user switches back to "All Articles"
- **THEN** the combined view SHALL be restored with feed name prefixes

#### Scenario: Articles with same publish date
- **WHEN** multiple articles have the same published_date
- **THEN** articles SHALL be sorted alphabetically by feed name
- **AND** articles from the same feed SHALL be sorted alphabetically by title
- **AND** sort order SHALL be consistent and deterministic

#### Scenario: No articles available
- **WHEN** "All Articles" is selected and no articles exist in any feed
- **THEN** an empty state message SHALL be displayed
- **AND** the message SHALL indicate "No articles yet. Press 'u' to fetch."

#### Scenario: Article interaction from combined view
- **WHEN** a user selects an article from the "All Articles" view
- **THEN** the article reader SHALL display the full article content
- **AND** the article SHALL be openable with the same link
- **AND** the like/unlike functionality SHALL work correctly

#### Scenario: Performance with many articles
- **WHEN** the database contains more than 100 articles across all feeds
- **THEN** the combined view SHALL load and display within 1 second
- **AND** the article list SHALL scroll smoothly using Textual's virtualization

## MODIFIED Requirements

### Requirement: Feed List Display

The TUI SHALL display a list of subscribed RSS feeds in the left sidebar, with "All Articles" as the first option.

#### Scenario: Feed list rendering
- **WHEN** the TUI loads
- **THEN** "All Articles" SHALL be displayed at the top of the feed list
- **AND** "All Articles" SHALL show the total article count in parentheses
- **AND** each individual feed SHALL be displayed below "All Articles"
- **AND** each feed SHALL show its name and article count in the format "Name (count)"

#### Scenario: Feed selection
- **WHEN** a user clicks on "All Articles"
- **THEN** a FeedSelected message SHALL be emitted with feed_id=0
- **WHEN** a user clicks on a specific feed
- **THEN** a FeedSelected message SHALL be emitted with that feed's ID
- **AND** the selected feed SHALL be highlighted

#### Scenario: Empty feed list
- **WHEN** no feeds are subscribed
- **THEN** "All Articles" SHALL still be displayed
- **AND** it SHALL show a count of 0
- **AND** selecting it SHALL show the empty state message
