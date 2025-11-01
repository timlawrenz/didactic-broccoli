# RSS Fetcher Specification

## ADDED Requirements

### Requirement: RSS Feed Parsing
The system SHALL fetch and parse RSS/Atom feeds using `feedparser`, extracting article metadata including title, link, summary, and published date.

#### Scenario: Successful feed fetch
- **WHEN** a valid RSS feed URL is provided
- **THEN** the feed is fetched and parsed into a list of article entries

#### Scenario: Article metadata extraction
- **WHEN** a feed is parsed
- **THEN** each article has title, link, summary, and published_date extracted

#### Scenario: Missing metadata handling
- **WHEN** an article is missing required fields (title or link)
- **THEN** that article is skipped with a warning logged

### Requirement: Article Text Extraction
The system SHALL extract full article text from web pages using `newspaper3k` for better content quality beyond RSS summaries.

#### Scenario: Full text extraction
- **WHEN** an article link is processed
- **THEN** the full article text is extracted from the web page

#### Scenario: Extraction failure fallback
- **WHEN** full text extraction fails (paywall, JavaScript-heavy site)
- **THEN** the system stores only the RSS summary and continues processing

### Requirement: Error Handling
The system SHALL handle network errors and malformed feeds gracefully without crashing the application.

#### Scenario: Network timeout
- **WHEN** a feed URL times out or is unreachable
- **THEN** an error is logged and the feed is skipped

#### Scenario: Invalid RSS format
- **WHEN** a URL returns non-RSS content
- **THEN** an error is logged and no articles are processed

#### Scenario: HTTP error codes
- **WHEN** a feed returns 404 or 500 status
- **THEN** the error is logged with the status code and feed is skipped

### Requirement: Fetch Pipeline
The system SHALL provide an orchestrated pipeline that fetches feeds, extracts articles, and stores them in the database atomically.

#### Scenario: End-to-end fetch
- **WHEN** `fetch_and_store_feed(feed_id)` is called
- **THEN** the feed is fetched, articles are extracted, stored in the database, and a count of new articles is returned

#### Scenario: Partial success handling
- **WHEN** some articles fail extraction during a feed fetch
- **THEN** successful articles are stored and failed ones are logged without blocking the batch

### Requirement: Idempotency
The system SHALL handle re-fetching feeds without creating duplicate articles, using the article link as a deduplication key.

#### Scenario: Re-fetch with no new articles
- **WHEN** a feed is fetched again with no new content
- **THEN** no duplicate articles are created and zero new articles are reported

#### Scenario: Re-fetch with new articles
- **WHEN** a feed is fetched again with some new articles
- **THEN** only new articles are added and existing ones are preserved
