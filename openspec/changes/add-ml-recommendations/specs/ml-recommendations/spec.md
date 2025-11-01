# ML Recommendations Specification

## ADDED Requirements

### Requirement: Embedding Generation
The system SHALL generate semantic embeddings for all articles to enable similarity search.

#### Scenario: Generate embedding on article fetch
- **WHEN** a new article is fetched from a feed
- **THEN** a 384-dimensional embedding vector is generated from the article text
- **AND** the embedding is stored in the embeddings table

#### Scenario: Handle embedding generation failure
- **WHEN** embedding generation fails for an article
- **THEN** the article is still stored without an embedding
- **AND** a warning is logged
- **AND** other articles continue processing

### Requirement: Taste Profile Learning
The system SHALL learn user taste profiles from liked articles using K-Means clustering.

#### Scenario: Calculate centroids from liked articles
- **WHEN** a user has liked 5 or more articles
- **THEN** K-Means clustering (k=5) creates taste centroids from the embeddings

#### Scenario: Handle few liked articles
- **WHEN** a user has liked fewer than 5 articles
- **THEN** the system uses k = number_of_liked_articles for clustering

#### Scenario: No liked articles
- **WHEN** a user has not liked any articles
- **THEN** the system shows a message to like articles first

### Requirement: Recommendation Generation
The system SHALL generate personalized article recommendations based on user taste profiles.

#### Scenario: Generate recommendations
- **WHEN** a user presses 'r' in the TUI
- **THEN** the system calculates taste centroids from liked articles
- **AND** finds the 50 most similar unread articles using vector search
- **AND** displays them ranked by similarity score

#### Scenario: Filter already-read articles
- **WHEN** generating recommendations
- **THEN** articles the user has already viewed are excluded from results

#### Scenario: Recommendations completed quickly
- **WHEN** recommendations are requested
- **THEN** results are displayed within 1 second

### Requirement: Vector Similarity Search
The system SHALL efficiently search for similar articles using vector embeddings.

#### Scenario: Find similar articles
- **WHEN** searching for articles similar to taste centroids
- **THEN** cosine similarity is used to rank articles
- **AND** the top N most similar articles are returned

#### Scenario: Scale to thousands of articles
- **WHEN** the database contains 1000+ articles
- **THEN** vector search completes in under 100ms

### Requirement: Model Management
The system SHALL manage the ML model lifecycle efficiently.

#### Scenario: Lazy load embedding model
- **WHEN** embeddings are first needed
- **THEN** the sentence-transformers model is loaded once
- **AND** cached for subsequent use

#### Scenario: Model download on first use
- **WHEN** the embedding model is not cached locally
- **THEN** it is downloaded automatically (~80MB)
- **AND** a progress indicator is shown

#### Scenario: Handle missing dependencies
- **WHEN** sentence-transformers is not installed
- **THEN** a clear error message is shown
- **AND** installation instructions are provided

### Requirement: TUI Recommendations View
The system SHALL display recommendations in an accessible TUI view.

#### Scenario: Show recommendations
- **WHEN** the user presses 'r' with sufficient liked articles
- **THEN** a recommendations view shows the top 50 articles
- **AND** each article displays its title, feed name, and similarity score

#### Scenario: Navigate recommendations
- **WHEN** in the recommendations view
- **THEN** the user can navigate with arrow keys or j/k
- **AND** select an article to read it

#### Scenario: Return to main view
- **WHEN** the user presses Escape or q in recommendations view
- **THEN** they return to the main feed/article view

#### Scenario: Not enough data message
- **WHEN** the user presses 'r' with fewer than 5 liked articles
- **THEN** a message displays: "Like at least 5 articles to get recommendations"

### Requirement: Database Storage
The system SHALL store embeddings efficiently in the database.

#### Scenario: Store embedding with article
- **WHEN** an article embedding is generated
- **THEN** it is stored in the embeddings table linked to the article_id

#### Scenario: Cascade delete embeddings
- **WHEN** an article is deleted
- **THEN** its embedding is automatically deleted via foreign key cascade

#### Scenario: Retrieve embeddings efficiently
- **WHEN** multiple embeddings are needed for clustering
- **THEN** they are retrieved in a single database query

### Requirement: Performance Optimization
The system SHALL optimize ML operations for CPU-only systems.

#### Scenario: Batch embedding generation
- **WHEN** multiple new articles are fetched
- **THEN** embeddings can be generated in parallel (future enhancement)

#### Scenario: Cache taste centroids
- **WHEN** taste centroids are calculated
- **THEN** they are cached until the user likes a new article
- **AND** subsequent recommendation requests reuse cached centroids

#### Scenario: Limit search space
- **WHEN** searching for similar articles
- **THEN** the search is limited to unread articles only
- **AND** already-liked articles are excluded
