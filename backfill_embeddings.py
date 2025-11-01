#!/usr/bin/env python3
"""Backfill embeddings for existing articles."""

import logging
from rss_reader.db import get_connection
from rss_reader.ml import generate_article_embedding, store_embedding

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def backfill_embeddings():
    """Generate embeddings for articles that don't have them."""
    conn = get_connection()
    
    # Find articles without embeddings
    cursor = conn.execute("""
        SELECT a.article_id, a.title, a.summary, a.full_text
        FROM articles a
        LEFT JOIN embeddings e ON a.article_id = e.article_id
        WHERE e.article_id IS NULL
    """)
    
    articles = cursor.fetchall()
    
    if not articles:
        logger.info("All articles already have embeddings")
        return
    
    logger.info(f"Generating embeddings for {len(articles)} articles...")
    
    success_count = 0
    for row in articles:
        article_id = row[0]
        article = {
            'title': row[1],
            'summary': row[2],
            'full_text': row[3]
        }
        
        try:
            embedding = generate_article_embedding(article)
            if embedding is not None:
                store_embedding(article_id, embedding)
                success_count += 1
                if success_count % 10 == 0:
                    logger.info(f"  Progress: {success_count}/{len(articles)}")
            else:
                logger.warning(f"  Failed to generate embedding for article {article_id}")
        except Exception as e:
            logger.error(f"  Error processing article {article_id}: {e}")
    
    logger.info(f"✓ Successfully generated {success_count}/{len(articles)} embeddings")

if __name__ == "__main__":
    backfill_embeddings()
