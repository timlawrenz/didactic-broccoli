# Design: Tavily API Article Extraction

## Context

The RSS reader currently uses `newspaper3k` for extracting full article text from URLs. While functional, newspaper3k has several limitations:
- Struggles with modern JavaScript-heavy websites
- Often fails on sites with dynamic content
- Limited paywall support
- Maintenance concerns (last updated 2020)
- Inconsistent extraction quality

Tavily's Extract API provides a more robust, API-based solution that can handle complex modern websites with higher success rates.

## Goals / Non-Goals

### Goals
- Improve article extraction success rate
- Better handle modern dynamic websites
- Maintain backward compatibility with newspaper3k
- Optional integration (no required dependency)
- Simple configuration via environment variable
- Graceful fallback when Tavily unavailable

### Non-Goals
- Remove newspaper3k (keep as fallback)
- Require Tavily API key for app to work
- Batch extraction optimization
- Caching extracted content
- Custom extraction rules per domain

## Decisions

### Decision: Use Tavily as Primary, newspaper3k as Fallback

Try Tavily extraction first when API key available, fall back to newspaper3k on failure.

**Rationale:**
- Best of both worlds approach
- No regression if Tavily fails
- Higher success rate with Tavily
- No breaking changes for existing users
- Smooth migration path

**Implementation:**
```python
def extract_article_text(url: str) -> str | None:
    # Try Tavily first if available
    if tavily_client:
        content = extract_with_tavily(url)
        if content:
            logger.info(f"Extracted with Tavily: {url}")
            return content
    
    # Fall back to newspaper3k
    content = extract_with_newspaper(url)
    if content:
        logger.info(f"Extracted with newspaper3k: {url}")
        return content
    
    return None
```

### Decision: Optional Dependency via pyproject.toml

Add `tavily-python` as optional dependency, not required.

**Rationale:**
- Users can choose to install it
- Doesn't force API key requirement
- Reduces install size for users who don't need it
- Follows Python best practices

**Implementation:**
```toml
[project.optional-dependencies]
tavily = ["tavily-python>=0.3.0"]
```

**Installation:**
```bash
pip install -e ".[tavily]"  # With Tavily
pip install -e .            # Without Tavily
```

### Decision: Environment Variable Configuration

Use `TAVILY_API_KEY` environment variable for API key.

**Rationale:**
- Standard practice for API keys
- Secure (not in code)
- Easy to configure
- Works with .env files
- Familiar pattern

**Configuration:**
```bash
# .env
TAVILY_API_KEY=tvly-your-api-key-here
```

### Decision: Initialize Client Lazily

Only initialize Tavily client if API key is present.

**Rationale:**
- No error if key missing
- No import error if library not installed
- Simple conditional logic
- Clear logging of availability

**Implementation:**
```python
tavily_client = None

def _initialize_tavily():
    global tavily_client
    api_key = os.getenv("TAVILY_API_KEY")
    if api_key:
        try:
            from tavily import TavilyClient
            tavily_client = TavilyClient(api_key=api_key)
            logger.info("Tavily client initialized")
        except ImportError:
            logger.warning("tavily-python not installed, using newspaper3k only")
        except Exception as e:
            logger.warning(f"Failed to initialize Tavily: {e}")
```

### Decision: Use tavily.extract() Method

Use the Extract API endpoint for article content extraction.

**Rationale:**
- Purpose-built for article extraction
- Returns clean, formatted content
- Handles complex websites automatically
- Single API call
- Good documentation

**API Call:**
```python
def extract_with_tavily(url: str) -> str | None:
    try:
        response = tavily_client.extract(urls=[url])
        if response and response.get("results"):
            result = response["results"][0]
            return result.get("raw_content")
    except Exception as e:
        logger.warning(f"Tavily extraction failed for {url}: {e}")
    return None
```

**Response Format:**
```json
{
  "results": [
    {
      "url": "https://example.com/article",
      "raw_content": "Full article text here...",
    }
  ],
  "failed_results": []
}
```

## Component Changes

### Fetcher Module (`rss_reader/fetcher.py`)

**Add Tavily client initialization:**
```python
import os
import logging

logger = logging.getLogger(__name__)
tavily_client = None

def _initialize_tavily():
    """Initialize Tavily client if API key available."""
    global tavily_client
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        logger.info("TAVILY_API_KEY not set, using newspaper3k only")
        return
    
    try:
        from tavily import TavilyClient
        tavily_client = TavilyClient(api_key=api_key)
        logger.info("Tavily client initialized successfully")
    except ImportError:
        logger.warning("tavily-python not installed. Install with: pip install tavily-python")
    except Exception as e:
        logger.error(f"Failed to initialize Tavily client: {e}")

# Initialize on module load
_initialize_tavily()
```

**Add Tavily extraction function:**
```python
def extract_with_tavily(url: str) -> str | None:
    """Extract article text using Tavily API.
    
    Args:
        url: Article URL to extract
        
    Returns:
        Extracted article text or None if failed
    """
    if not tavily_client:
        return None
    
    try:
        logger.debug(f"Extracting with Tavily: {url}")
        response = tavily_client.extract(urls=[url])
        
        if not response or "results" not in response:
            logger.warning(f"Tavily returned empty response for {url}")
            return None
        
        results = response["results"]
        if not results:
            logger.warning(f"Tavily found no results for {url}")
            return None
        
        result = results[0]
        content = result.get("raw_content")
        
        if content:
            logger.info(f"Successfully extracted {len(content)} chars with Tavily: {url}")
            return content
        else:
            logger.warning(f"Tavily returned no content for {url}")
            return None
            
    except Exception as e:
        logger.warning(f"Tavily extraction failed for {url}: {e}")
        return None
```

**Update existing extraction function:**
```python
def extract_article_text(url: str) -> str | None:
    """Extract article text from URL.
    
    Tries Tavily API first if available, falls back to newspaper3k.
    
    Args:
        url: Article URL
        
    Returns:
        Extracted article text or None
    """
    # Try Tavily first if available
    if tavily_client:
        content = extract_with_tavily(url)
        if content:
            return content
        logger.info(f"Tavily failed, falling back to newspaper3k: {url}")
    
    # Fall back to newspaper3k
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        if article.text:
            logger.info(f"Successfully extracted {len(article.text)} chars with newspaper3k: {url}")
            return article.text
        else:
            logger.warning(f"newspaper3k extracted no text: {url}")
            return None
            
    except Exception as e:
        logger.error(f"Failed to extract article from {url}: {e}")
        return None
```

### Dependencies (`pyproject.toml`)

**Add optional dependency:**
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
]
tavily = [
    "tavily-python>=0.3.0",
]
```

### Environment Configuration

**Create `.env.example`:**
```bash
# Tavily API for article extraction (optional)
# Get your API key from: https://tavily.com
TAVILY_API_KEY=tvly-your-api-key-here
```

## Error Handling

### API Key Missing
- Client not initialized
- Fall back to newspaper3k silently
- Log info message

### API Key Invalid
- Tavily initialization fails
- Log warning
- Fall back to newspaper3k

### API Rate Limit
- Tavily returns 429 error
- Log warning with rate limit info
- Fall back to newspaper3k for this article

### Network Timeout
- Tavily request times out
- Log warning
- Fall back to newspaper3k

### Malformed URL
- Tavily returns error
- Log warning
- Fall back to newspaper3k

### Empty Content
- Tavily returns empty raw_content
- Log warning
- Fall back to newspaper3k

## Testing Strategy

### Unit Tests
```python
def test_extract_with_tavily_success(mocker):
    """Test successful Tavily extraction."""
    mock_client = mocker.Mock()
    mock_client.extract.return_value = {
        "results": [{"raw_content": "Article content"}]
    }
    
    content = extract_with_tavily("https://example.com/article")
    assert content == "Article content"

def test_extract_with_tavily_failure(mocker):
    """Test Tavily extraction failure falls back."""
    mock_client = mocker.Mock()
    mock_client.extract.side_effect = Exception("API error")
    
    content = extract_with_tavily("https://example.com/article")
    assert content is None
```

### Integration Tests
- Test with real Tavily API key (if available)
- Test without API key (newspaper3k fallback)
- Test with complex modern website
- Test with simple website
- Test rate limit handling

### Manual Testing
1. Set TAVILY_API_KEY → verify Tavily used
2. Unset API key → verify newspaper3k used
3. Set invalid key → verify graceful fallback
4. Test with various article URLs

## Performance Considerations

### API Latency
- Tavily API call: ~1-3 seconds
- Similar to newspaper3k scraping
- Acceptable for background fetching
- No impact on TUI responsiveness

### Rate Limits
- Tavily free tier: 1000 requests/month
- Typical usage: 10-50 articles/day = 300-1500/month
- May need paid plan for heavy users
- Fallback prevents complete failure

### Error Rate
- Tavily typically higher success rate than newspaper3k
- Fallback ensures no regression
- Logging tracks which method works

## Migration Plan

### Phase 1: Optional Installation
- Add to pyproject.toml
- Document in README
- No changes for existing users

### Phase 2: Gradual Adoption
- Users install tavily-python when ready
- Add API key to .env
- Automatic activation

### Phase 3: Monitor & Optimize
- Track success rates
- Compare Tavily vs newspaper3k
- Adjust priority if needed

## Alternatives Considered

### Alternative: Remove newspaper3k Entirely

Use only Tavily API.

**Rejected because:**
- Requires API key (breaking change)
- No fallback if API down
- Costs money for heavy users
- Less flexible

### Alternative: Make Tavily Required Dependency

Install tavily-python by default.

**Rejected because:**
- Increases install size
- Not needed without API key
- Forces dependency on all users

### Alternative: Custom Scraping

Build custom web scraper.

**Rejected because:**
- Reinventing the wheel
- Hard to maintain
- Many edge cases
- Tavily already solves this

### Alternative: Use Jina Reader API

Alternative API-based extraction.

**Rejected because:**
- Less documentation
- Fewer features
- Tavily more popular
- Can be added later if needed

## Risks / Trade-offs

### Risk: API Costs

**Mitigation:**
- Optional feature
- Free tier adequate for most users
- Fallback to free newspaper3k
- Document costs in README

### Risk: API Downtime

**Mitigation:**
- Automatic fallback to newspaper3k
- No complete failure
- Logging tracks issues

### Risk: Vendor Lock-in

**Mitigation:**
- Newspaper3k still available
- Easy to add alternative APIs
- Abstraction layer for extraction

### Trade-off: External Dependency

Adding API dependency vs better extraction.

**Acceptable because:**
- Optional (not required)
- Significant quality improvement
- Industry standard approach
- Graceful fallback

## Open Questions

- [ ] Should we cache Tavily extractions to save API calls?
- [ ] Should we add configuration for extraction timeout?
- [ ] Should we support batch extraction for multiple URLs?
- [ ] Should we add metrics dashboard for extraction success rates?

## Sign-Off Criteria

- [ ] Tavily extraction works when API key provided
- [ ] Falls back to newspaper3k when Tavily unavailable
- [ ] No errors when tavily-python not installed
- [ ] No errors when TAVILY_API_KEY not set
- [ ] Extraction success rate improved
- [ ] All existing tests pass
- [ ] New tests added for Tavily extraction
- [ ] README updated with configuration instructions
- [ ] .env.example created with API key placeholder
