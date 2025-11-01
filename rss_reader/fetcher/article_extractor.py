"""Article full-text extraction from web pages."""

import logging
from typing import Optional

from newspaper import Article


logger = logging.getLogger(__name__)


def extract_article_text(url: str) -> Optional[str]:
    """Extract full article text from web page.
    
    Args:
        url: Article URL
        
    Returns:
        Extracted article text, or None if extraction fails
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        if article.text:
            logger.info(f"Extracted {len(article.text)} characters from {url}")
            return article.text
        else:
            logger.warning(f"No text extracted from {url}")
            return None
            
    except Exception as e:
        logger.warning(f"Failed to extract article from {url}: {e}")
        return None
