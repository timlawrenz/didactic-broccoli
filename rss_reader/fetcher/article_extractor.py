"""Article full-text extraction from web pages."""

import logging
import os
from typing import Optional

from newspaper import Article


logger = logging.getLogger(__name__)

# Tavily client (initialized lazily if API key available)
tavily_client = None


def _initialize_tavily():
    """Initialize Tavily client if API key is available."""
    global tavily_client
    
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        logger.info("TAVILY_API_KEY not set, using newspaper3k only for article extraction")
        return
    
    try:
        from tavily import TavilyClient
        tavily_client = TavilyClient(api_key=api_key)
        logger.info("Tavily client initialized successfully for article extraction")
    except ImportError:
        logger.warning("tavily-python not installed. Install with: pip install -e '.[tavily]'")
    except Exception as e:
        logger.error(f"Failed to initialize Tavily client: {e}")


# Initialize on module load
_initialize_tavily()


def extract_with_tavily(url: str) -> Optional[str]:
    """Extract article text using Tavily API.
    
    Args:
        url: Article URL to extract
        
    Returns:
        Extracted article text or None if failed
    """
    if not tavily_client:
        return None
    
    try:
        logger.debug(f"Attempting Tavily extraction: {url}")
        # Tavily Extract accepts multiple URLs, but we'll use one at a time for now
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
            logger.info(f"Successfully extracted {len(content)} characters with Tavily: {url}")
            return content
        else:
            logger.warning(f"Tavily returned no content for {url}")
            return None
            
    except Exception as e:
        logger.warning(f"Tavily extraction failed for {url}: {e}")
        return None


def extract_article_text(url: str) -> Optional[str]:
    """Extract full article text from web page.
    
    Tries Tavily API first if available, falls back to newspaper3k.
    
    Args:
        url: Article URL
        
    Returns:
        Extracted article text, or None if extraction fails
    """
    # Try Tavily first if available
    if tavily_client:
        content = extract_with_tavily(url)
        if content:
            return content
        logger.info(f"Tavily extraction failed, falling back to newspaper3k: {url}")
    
    # Fall back to newspaper3k
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        if article.text:
            logger.info(f"Extracted {len(article.text)} characters with newspaper3k: {url}")
            return article.text
        else:
            logger.warning(f"No text extracted from {url}")
            return None
            
    except Exception as e:
        logger.warning(f"Failed to extract article from {url}: {e}")
        return None
