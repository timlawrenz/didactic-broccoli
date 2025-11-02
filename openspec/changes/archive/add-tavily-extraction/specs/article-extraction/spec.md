## ADDED Requirements

### Requirement: Optional Tavily API Article Extraction

The system SHALL support optional article extraction using the Tavily API when configured, with graceful fallback to newspaper3k.

#### Scenario: Extract with Tavily when API key configured
- **WHEN** TAVILY_API_KEY environment variable is set
- **AND** tavily-python library is installed
- **AND** an article URL needs to be extracted
- **THEN** the system SHALL attempt extraction using Tavily API
- **AND** the system SHALL use the tavily.extract() method
- **AND** the system SHALL return the raw_content from the API response

#### Scenario: Fall back to newspaper3k when Tavily unavailable
- **WHEN** TAVILY_API_KEY is not set
- **OR** tavily-python is not installed
- **OR** Tavily API returns an error
- **THEN** the system SHALL fall back to newspaper3k extraction
- **AND** the system SHALL log which extraction method was used
- **AND** extraction SHALL succeed if newspaper3k can extract the content

#### Scenario: Handle Tavily API errors gracefully
- **WHEN** Tavily API returns an error (rate limit, network, invalid URL)
- **THEN** the system SHALL log a warning with the error details
- **AND** the system SHALL fall back to newspaper3k extraction
- **AND** no exceptions SHALL be raised to calling code

#### Scenario: Initialize Tavily client on module load
- **WHEN** the fetcher module is loaded
- **AND** TAVILY_API_KEY environment variable is set
- **THEN** the system SHALL initialize a TavilyClient instance
- **AND** the system SHALL log successful initialization
- **WHEN** TAVILY_API_KEY is not set
- **THEN** the system SHALL log that newspaper3k only will be used
- **AND** no errors SHALL occur

#### Scenario: Extract article content from URL
- **WHEN** extract_article_text() is called with a URL
- **AND** Tavily client is initialized
- **THEN** the system SHALL call tavily_client.extract() with the URL
- **AND** the system SHALL parse the response for raw_content
- **AND** the system SHALL return the extracted text content
- **WHEN** raw_content is present and valid
- **THEN** the system SHALL log the extraction success with content length

#### Scenario: Handle empty Tavily response
- **WHEN** Tavily API returns empty results
- **OR** raw_content field is missing or empty
- **THEN** the system SHALL log a warning
- **AND** the system SHALL return None to trigger fallback
- **AND** newspaper3k extraction SHALL be attempted

#### Scenario: Track extraction method used
- **WHEN** an article is successfully extracted
- **THEN** the system SHALL log which method succeeded (Tavily or newspaper3k)
- **AND** the log SHALL include the URL and content length
- **AND** developers SHALL be able to track extraction success rates

#### Scenario: Optional dependency installation
- **WHEN** a user installs the package with pip install -e ".[tavily]"
- **THEN** tavily-python SHALL be installed
- **WHEN** a user installs without optional dependencies
- **THEN** tavily-python SHALL not be installed
- **AND** the system SHALL work with newspaper3k only
- **AND** no import errors SHALL occur

#### Scenario: API key configuration
- **WHEN** a user sets TAVILY_API_KEY in .env file
- **THEN** the environment variable SHALL be loaded on app start
- **AND** Tavily client SHALL be initialized with the key
- **WHEN** the API key is invalid or expired
- **THEN** initialization SHALL fail gracefully
- **AND** the system SHALL fall back to newspaper3k

#### Scenario: Performance with API calls
- **WHEN** extracting articles with Tavily API
- **THEN** each extraction SHALL complete within 5 seconds
- **AND** API latency SHALL not block the TUI
- **AND** background fetching SHALL handle timeouts gracefully

## MODIFIED Requirements

### Requirement: Article Text Extraction

The system SHALL extract full article text from URLs using available extraction methods with automatic fallback.

#### Scenario: Extraction priority and fallback
- **WHEN** an article URL needs to be extracted
- **THEN** the system SHALL try Tavily API first if available
- **WHEN** Tavily extraction fails or is unavailable
- **THEN** the system SHALL try newspaper3k extraction
- **WHEN** both methods fail
- **THEN** the system SHALL return None and log the failure
- **AND** the article SHALL still be stored with summary only

#### Scenario: Extraction method logging
- **WHEN** an article is extracted successfully
- **THEN** the system SHALL log which extraction method was used
- **AND** the log level SHALL be INFO for success
- **AND** the log level SHALL be WARNING for fallback
- **AND** the log level SHALL be ERROR for complete failure
