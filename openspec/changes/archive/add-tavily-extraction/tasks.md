# Implementation Tasks

## 1. Dependencies & Configuration
- [x] 1.1 Add `tavily-python` to pyproject.toml as optional dependency
- [x] 1.2 Add TAVILY_API_KEY to environment variable handling
- [x] 1.3 Create .env.example with TAVILY_API_KEY placeholder
- [x] 1.4 Update README with Tavily configuration instructions
- [x] 1.5 Test installation with optional dependency

## 2. Tavily Client Setup
- [x] 2.1 Create TavilyClient initialization in fetcher module
- [x] 2.2 Check for TAVILY_API_KEY environment variable
- [x] 2.3 Initialize client only if key is available
- [x] 2.4 Handle missing or invalid API key gracefully
- [x] 2.5 Add logging for Tavily availability

## 3. Extract Function Implementation
- [x] 3.1 Create extract_with_tavily() function
- [x] 3.2 Call tavily.extract() with article URL
- [x] 3.3 Parse response to get raw_content
- [x] 3.4 Handle API errors (rate limits, network, invalid URL)
- [x] 3.5 Return None on failure for fallback

## 4. Integration with Existing Extraction
- [x] 4.1 Modify extract_article_text() to try Tavily first
- [x] 4.2 Fall back to newspaper3k if Tavily fails or unavailable
- [x] 4.3 Add logging to track which method succeeded
- [x] 4.4 Preserve existing error handling
- [x] 4.5 Test extraction priority (Tavily → newspaper3k)

## 5. Error Handling & Edge Cases
- [x] 5.1 Handle API rate limits gracefully
- [x] 5.2 Handle network timeouts
- [x] 5.3 Handle invalid/malformed URLs
- [x] 5.4 Handle API key expiration or quota exceeded
- [x] 5.5 Handle empty extraction results

## 6. Testing
- [x] 6.1 Test with TAVILY_API_KEY set (successful extraction)
- [x] 6.2 Test without TAVILY_API_KEY (falls back to newspaper3k)
- [x] 6.3 Test with invalid API key (falls back gracefully)
- [x] 6.4 Test with URL that Tavily can't extract
- [x] 6.5 Test with complex modern website
- [x] 6.6 Add unit tests for extract_with_tavily()
- [x] 6.7 Update integration tests

## 7. Documentation
- [x] 7.1 Add Tavily section to README
- [x] 7.2 Explain how to get Tavily API key
- [x] 7.3 Document extraction fallback behavior
- [x] 7.4 Add example .env configuration
- [x] 7.5 Update installation instructions for optional dependencies

## 8. Performance & Monitoring
- [x] 8.1 Add metrics logging for extraction method used
- [x] 8.2 Track success rates for Tavily vs newspaper3k
- [x] 8.3 Monitor API usage for rate limits
- [x] 8.4 Verify no performance degradation
