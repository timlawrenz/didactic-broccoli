## MODIFIED Requirements

### Requirement: Article Reader Display

The TUI SHALL display article content in a readable format with proper word-wrapping.

#### Scenario: Display article with word-wrap
- **WHEN** an article is loaded in the reader panel
- **THEN** the article title SHALL be displayed in bold
- **AND** metadata (date, link, liked status) SHALL be displayed
- **AND** article text SHALL wrap at panel boundaries
- **AND** no horizontal scrolling SHALL be required

#### Scenario: Long paragraphs wrap correctly
- **WHEN** an article contains paragraphs longer than the panel width
- **THEN** text SHALL wrap at word boundaries
- **AND** lines SHALL not extend beyond the panel edge
- **AND** text SHALL remain fully readable

#### Scenario: Vertical scrolling for long articles
- **WHEN** article content exceeds the panel height
- **THEN** vertical scrolling SHALL be available
- **AND** the user SHALL be able to scroll with mouse wheel, arrow keys, or page up/down
- **AND** vim-style scrolling (ctrl+u/ctrl+d) SHALL work

#### Scenario: Responsive text reflow
- **WHEN** the terminal window is resized
- **THEN** article text SHALL automatically reflow to fit the new width
- **AND** no text SHALL be cut off or hidden
- **AND** vertical scroll position SHALL be maintained if possible

#### Scenario: Handle long URLs
- **WHEN** an article contains URLs longer than panel width
- **THEN** URLs SHALL wrap to multiple lines
- **AND** the full URL SHALL remain visible and copyable
- **AND** URL wrapping SHALL not break readability

#### Scenario: Preserve text formatting
- **WHEN** an article is displayed with word-wrap enabled
- **THEN** bold text (title) SHALL remain bold
- **AND** dim text (metadata) SHALL remain dim
- **AND** colored text (feed names in combined view) SHALL maintain colors
- **AND** paragraph breaks SHALL be preserved

#### Scenario: Empty or minimal content
- **WHEN** an article has no content available
- **THEN** a message "[dim]No content available[/dim]" SHALL be displayed
- **WHEN** an article has only a title and no body text
- **THEN** the title and metadata SHALL be displayed without errors
