#!/usr/bin/env python3
"""Demo script showing basic RSS reader functionality."""

import logging
from rss_reader.db import add_feed, get_all_feeds, get_articles_by_feed, like_article, get_liked_articles
from rss_reader.fetcher import fetch_and_store_feed

# Enable logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    print("=" * 60)
    print("RSS Reader Demo")
    print("=" * 60)
    
    # Add a feed
    print("\n1. Adding Ars Technica RSS feed...")
    feed_id = add_feed(
        "https://feeds.arstechnica.com/arstechnica/index",
        "Ars Technica"
    )
    print(f"   ✓ Feed added with ID: {feed_id}")
    
    # Fetch articles
    print("\n2. Fetching articles from feed...")
    try:
        new_count = fetch_and_store_feed(feed_id)
        print(f"   ✓ Added {new_count} new articles")
    except Exception as e:
        print(f"   ✗ Error fetching feed: {e}")
        print("   (This is expected if you're offline)")
    
    # List all feeds
    print("\n3. Listing all subscribed feeds:")
    feeds = get_all_feeds()
    for feed in feeds:
        print(f"   - {feed['name']} ({feed['url']})")
    
    # List articles
    print(f"\n4. Showing recent articles from feed {feed_id}:")
    articles = get_articles_by_feed(feed_id, limit=5)
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"   {i}. {article['title']}")
            print(f"      Link: {article['link']}")
            if article['published_date']:
                print(f"      Published: {article['published_date']}")
            print()
    else:
        print("   (No articles fetched yet)")
    
    # Like an article
    if articles:
        article_id = articles[0]['article_id']
        print(f"\n5. Liking article ID {article_id}...")
        like_article(article_id)
        print("   ✓ Article liked!")
        
        print("\n6. Showing liked articles:")
        liked = get_liked_articles()
        for article in liked:
            print(f"   - {article['title']}")
    
    print("\n" + "=" * 60)
    print("Demo complete! Database saved to: rss_reader.db")
    print("=" * 60)

if __name__ == "__main__":
    main()
