"""Simple demo to verify basic functionality works."""
from rss_reader.db import get_all_feeds, get_articles_by_feed

print("=== RSS Reader Data Check ===\n")

feeds = get_all_feeds()
print(f"Total feeds: {len(feeds)}\n")

for feed in feeds:
    articles = get_articles_by_feed(feed['feed_id'], limit=5)
    print(f"Feed: {feed['name']}")
    print(f"  URL: {feed['url']}")
    print(f"  Articles: {len(articles)}")
    if articles:
        print(f"  Latest: {articles[0]['title'][:50]}...")
    print()
