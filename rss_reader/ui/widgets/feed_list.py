"""Feed list widget for sidebar."""

import logging
from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.containers import VerticalScroll, Vertical
from textual.message import Message
from textual.reactive import reactive

from ...db import get_all_feeds, get_articles_by_feed, get_all_articles_sorted


logger = logging.getLogger(__name__)


class FeedItem(Static):
    """A single feed item that can be selected."""
    
    DEFAULT_CSS = """
    FeedItem {
        width: 100%;
        height: auto;
        padding: 1;
        border-bottom: solid $panel;
    }
    
    FeedItem:hover {
        background: $boost;
    }
    """
    
    def __init__(self, feed_id: int, feed_name: str, article_count: int, is_all_articles: bool = False):
        super().__init__()
        self.feed_id = feed_id
        self.feed_name = feed_name
        self.article_count = article_count
        self.is_all_articles = is_all_articles
    
    def render(self) -> str:
        """Render the feed item."""
        if self.is_all_articles:
            # Bold/highlighted for "All Articles"
            return f"[bold]📰 {self.feed_name}[/bold] [dim]({self.article_count})[/dim]"
        return f"{self.feed_name} [dim]({self.article_count})[/dim]"
    
    async def on_click(self) -> None:
        """Handle click on feed item."""
        # Find the FeedList parent
        parent = self.parent
        while parent and not isinstance(parent, FeedList):
            parent = parent.parent
        if parent:
            parent.post_message(FeedList.FeedSelected(self.feed_id, self.feed_name))


class FeedList(Vertical):
    """Widget displaying subscribed feeds."""
    
    DEFAULT_CSS = """
    FeedList {
        width: 100%;
        height: 100%;
    }
    
    FeedList #feed-container {
        height: 1fr;
        overflow-y: auto;
    }
    """
    
    class FeedSelected(Message):
        """Message sent when a feed is selected."""
        
        def __init__(self, feed_id: int, feed_name: str) -> None:
            self.feed_id = feed_id
            self.feed_name = feed_name
            super().__init__()
    
    selected_feed_id: reactive[int | None] = reactive(None)
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Label("📡 Feeds", id="feed-header")
        yield VerticalScroll(id="feed-container")
    
    def load_feeds(self) -> None:
        """Load feeds from database and populate list."""
        try:
            logger.info("load_feeds: Starting")
            container = self.query_one("#feed-container", VerticalScroll)
            logger.info(f"load_feeds: Found container: {container}")
            container.remove_children()
            
            feeds = get_all_feeds()
            logger.info(f"load_feeds: Got {len(feeds)} feeds from database")
            
            # Calculate total article count across all feeds
            total_count = 0
            feed_counts = {}
            
            for feed in feeds:
                articles = get_articles_by_feed(feed['feed_id'], limit=1000)
                count = len(articles)
                feed_counts[feed['feed_id']] = count
                total_count += count
            
            # Add "All Articles" as first item
            items = []
            all_articles_item = FeedItem(0, "All Articles", total_count, is_all_articles=True)
            items.append(all_articles_item)
            
            logger.info(f"load_feeds: Added 'All Articles' with {total_count} total articles")
            
            if not feeds:
                # Still show "All Articles" even with no feeds
                container.mount(*items)
                logger.info("Mounted only 'All Articles' (no feeds)")
                return
            
            # Add separator
            items.append(Label("[dim]─────────────────[/dim]"))
            
            # Mount each feed item
            for feed in feeds:
                count = feed_counts[feed['feed_id']]
                logger.info(f"load_feeds: Creating FeedItem for {feed['name']} with {count} articles")
                item = FeedItem(feed['feed_id'], feed['name'], count)
                items.append(item)
            
            # Mount all items at once
            container.mount(*items)
            
            logger.info(f"load_feeds: Successfully mounted {len(items)} items")
        except Exception as e:
            logger.error(f"load_feeds: Error - {e}", exc_info=True)
    
    def refresh_feeds(self) -> None:
        """Reload feeds from database."""
        self.load_feeds()
