# Database Layer Specification

## ADDED Requirements

### Requirement: SQLite Database Schema
The system SHALL use SQLite to store RSS feeds, articles, and user interactions with three core tables: `feeds`, `articles`, and `user_likes`.

#### Scenario: Database initialization
- **WHEN** the application starts for the first time
- **THEN** the SQLite database is created with all required tables and indexes

#### Scenario: Feed storage
- **WHEN** a new RSS feed is subscribed
- **THEN** it is stored in the `feeds` table with url, name, and timestamps

#### Scenario: Article storage
- **WHEN** articles are fetched from a feed
- **THEN** they are stored in `articles` with title, link, summary, full_text, and published_date

### Requirement: Data Integrity
The system SHALL enforce foreign key constraints and prevent duplicate articles using the `link` field as a unique identifier.

#### Scenario: Duplicate prevention
- **WHEN** an article with an existing link is fetched again
- **THEN** the duplicate is ignored without error

#### Scenario: Cascading deletes
- **WHEN** a feed is deleted
- **THEN** all associated articles and likes are automatically removed

### Requirement: Connection Management
The system SHALL provide a connection manager that handles SQLite connections with proper transaction management and cleanup.

#### Scenario: Transaction commit
- **WHEN** data is written to the database
- **THEN** changes are committed and persisted to disk

#### Scenario: Connection cleanup
- **WHEN** the application exits
- **THEN** all database connections are properly closed

### Requirement: CRUD Operations
The system SHALL provide data access methods for creating, reading, updating, and deleting feeds, articles, and user likes.

#### Scenario: Add feed
- **WHEN** `add_feed(url, name)` is called
- **THEN** a new feed record is created and feed_id is returned

#### Scenario: Fetch articles
- **WHEN** `get_articles_by_feed(feed_id)` is called
- **THEN** all articles for that feed are returned as a list

#### Scenario: Like article
- **WHEN** `like_article(article_id)` is called
- **THEN** a record is added to `user_likes` with user_id=1 and current timestamp

#### Scenario: Get liked articles
- **WHEN** `get_liked_articles()` is called
- **THEN** all articles the user has liked are returned

### Requirement: Single-User Design
The system SHALL default to user_id=1 for all user interactions, optimized for personal use.

#### Scenario: Implicit user context
- **WHEN** any user action is performed
- **THEN** it is associated with user_id=1 without requiring explicit user identification
