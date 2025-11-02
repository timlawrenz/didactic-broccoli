# Add Tavily API for Article Extraction

## Why

Currently, the RSS reader uses `newspaper3k` to extract full article text from URLs, but this library often fails on modern websites with dynamic content, paywalls, or complex JavaScript. Tavily's Extract API provides a more robust, API-based solution that can extract clean article content from virtually any URL with higher success rates and better formatting.

## What Changes

- Add optional Tavily API integration for article extraction
- Use Tavily Extract API as primary extraction method when API key is available
- Fall back to existing newspaper3k extraction if Tavily fails or is unavailable
- Add TAVILY_API_KEY configuration option
- Install `tavily-python` SDK as optional dependency
- Preserve existing extraction behavior when Tavily is not configured

## Impact

- Affected specs: article-extraction (new spec)
- Affected code:
  - `rss_reader/fetcher.py` - Add Tavily extraction method
  - `pyproject.toml` - Add tavily-python as optional dependency
  - `.env.example` or README - Document TAVILY_API_KEY configuration
- No breaking changes - purely additive with graceful fallback
- Significantly improved extraction success rate and quality
- Clean, formatted article content from complex websites

## Benefits

- **Higher success rate**: Tavily handles modern websites better than newspaper3k
- **Better content quality**: Cleaner extraction with proper formatting
- **Handles dynamic content**: Works with JavaScript-heavy sites
- **Paywall support**: Can extract from some paywalled content
- **Simple integration**: Single API call, no web scraping complexity
- **Graceful fallback**: Existing newspaper3k still works if Tavily unavailable
