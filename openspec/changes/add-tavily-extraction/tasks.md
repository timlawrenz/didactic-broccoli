# Implementation Tasks

## 1. Dependencies & Configuration
- [ ] 1.1 Add `tavily-python` to pyproject.toml as optional dependency
- [ ] 1.2 Add TAVILY_API_KEY to environment variable handling
- [ ] 1.3 Create .env.example with TAVILY_API_KEY placeholder
- [ ] 1.4 Update README with Tavily configuration instructions
- [ ] 1.5 Test installation with optional dependency

## 2. Tavily Client Setup
- [ ] 2.1 Create TavilyClient initialization in fetcher module
- [ ] 2.2 Check for TAVILY_API_KEY environment variable
- [ ] 2.3 Initialize client only if key is available
- [ ] 2.4 Handle missing or invalid API key gracefully
- [ ] 2.5 Add logging for Tavily availability

## 3. Extract Function Implementation
- [ ] 3.1 Create extract_with_tavily() function
- [ ] 3.2 Call tavily.extract() with article URL
- [ ] 3.3 Parse response to get raw_content
- [ ] 3.4 Handle API errors (rate limits, network, invalid URL)
- [ ] 3.5 Return None on failure for fallback

## 4. Integration with Existing Extraction
- [ ] 4.1 Modify extract_article_text() to try Tavily first
- [ ] 4.2 Fall back to newspaper3k if Tavily fails or unavailable
- [ ] 4.3 Add logging to track which method succeeded
- [ ] 4.4 Preserve existing error handling
- [ ] 4.5 Test extraction priority (Tavily → newspaper3k)

## 5. Error Handling & Edge Cases
- [ ] 5.1 Handle API rate limits gracefully
- [ ] 5.2 Handle network timeouts
- [ ] 5.3 Handle invalid/malformed URLs
- [ ] 5.4 Handle API key expiration or quota exceeded
- [ ] 5.5 Handle empty extraction results

## 6. Testing
- [ ] 6.1 Test with TAVILY_API_KEY set (successful extraction)
- [ ] 6.2 Test without TAVILY_API_KEY (falls back to newspaper3k)
- [ ] 6.3 Test with invalid API key (falls back gracefully)
- [ ] 6.4 Test with URL that Tavily can't extract
- [ ] 6.5 Test with complex modern website
- [ ] 6.6 Add unit tests for extract_with_tavily()
- [ ] 6.7 Update integration tests

## 7. Documentation
- [ ] 7.1 Add Tavily section to README
- [ ] 7.2 Explain how to get Tavily API key
- [ ] 7.3 Document extraction fallback behavior
- [ ] 7.4 Add example .env configuration
- [ ] 7.5 Update installation instructions for optional dependencies

## 8. Performance & Monitoring
- [ ] 8.1 Add metrics logging for extraction method used
- [ ] 8.2 Track success rates for Tavily vs newspaper3k
- [ ] 8.3 Monitor API usage for rate limits
- [ ] 8.4 Verify no performance degradation
