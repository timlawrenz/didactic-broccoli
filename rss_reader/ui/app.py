"""Main TUI application."""

import logging
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer
from textual.binding import Binding
from textual.worker import Worker, WorkerState

from ..db import add_feed, delete_feed, like_article, unlike_article, get_liked_articles, get_all_feeds
from ..fetcher import fetch_and_store_feed, FeedFetchError
from .widgets import FeedList, ArticleList, ArticleReader, AddFeedDialog, ConfirmDeleteDialog


logger = logging.getLogger(__name__)


class RSSReaderApp(App):
    """RSS Reader TUI application."""
    
    # Increase notification timeout to 5 seconds
    NOTIFICATION_TIMEOUT = 5.0
    
    CSS = """
    Screen {
        background: $background;
    }
    
    #feed-list {
        width: 25%;
        border-right: solid $accent;
        padding: 1;
        height: 100%;
    }
    
    #article-list {
        width: 35%;
        border-right: solid $accent;
        padding: 1;
        height: 100%;
    }
    
    #article-reader {
        width: 40%;
        padding: 1;
        height: 100%;
    }
    
    #feed-header, #article-header, #reader-header {
        background: $boost;
        padding: 1;
        margin-bottom: 1;
    }
    
    #feed-container {
        height: 1fr;
        overflow-y: auto;
    }
    
    .feed-item {
        width: 100%;
        height: auto;
        padding: 1;
        border-bottom: solid $panel;
    }
    
    .feed-item:hover {
        background: $boost;
    }
    
    #feed-listview, #article-listview {
        height: 100%;
    }
    
    #reader-container {
        height: 100%;
        overflow-y: auto;
    }
    
    #reader-content {
        padding: 1;
    }
    
    /* Dialog styles */
    #dialog-container {
        width: 60;
        height: auto;
        background: $surface;
        border: thick $primary;
        padding: 1;
    }
    
    #dialog-title {
        text-align: center;
        background: $boost;
        padding: 1;
        margin-bottom: 1;
    }
    
    #dialog-content {
        padding: 1;
    }
    
    .label {
        margin-top: 1;
    }
    
    Input {
        margin-bottom: 1;
    }
    
    .button-row {
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 2;
    }
    
    .button-row Button {
        margin: 0 1;
    }
    
    .error {
        color: $error;
        margin-top: 1;
        text-align: center;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("u", "update_feeds", "Update", show=True),
        Binding("l", "toggle_like", "Like", show=True),
        Binding("a", "add_feed", "Add", show=True),
        Binding("d", "delete_feed", "Delete", show=True),
        Binding("r", "recommendations", "Recs", show=True),
        Binding("j", "move_down", "Down", show=False),
        Binding("k", "move_up", "Up", show=False),
    ]
    
    TITLE = "RSS Reader"
    
    def compose(self) -> ComposeResult:
        """Create child widgets forming the UI."""
        yield Header()
        yield Horizontal(
            FeedList(id="feed-list"),
            ArticleList(id="article-list"),
            ArticleReader(id="article-reader"),
        )
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize app when mounted."""
        logger.info("RSS Reader TUI started")
        
        # Load feeds after a short delay to ensure UI is ready
        self.set_timer(0.1, self._load_initial_data)
    
    def _load_initial_data(self) -> None:
        """Load initial data after UI is ready."""
        logger.info("_load_initial_data called")
        try:
            feed_list = self.query_one("#feed-list", FeedList)
            logger.info(f"Found feed_list widget: {feed_list}")
            feed_list.load_feeds()
            logger.info("load_feeds() called successfully")
        except Exception as e:
            logger.error(f"Error in _load_initial_data: {e}", exc_info=True)
    
    def on_feed_list_feed_selected(self, message: FeedList.FeedSelected) -> None:
        """Handle feed selection."""
        article_list = self.query_one("#article-list", ArticleList)
        article_list.load_articles(message.feed_id)
    
    def on_article_list_article_selected(self, message: ArticleList.ArticleSelected) -> None:
        """Handle article selection."""
        reader = self.query_one("#article-reader", ArticleReader)
        reader.load_article(message.article_id, message.article)
    
    def action_move_down(self) -> None:
        """Move selection down (vim j key)."""
        focused = self.focused
        if focused and hasattr(focused, 'action_cursor_down'):
            focused.action_cursor_down()
    
    def action_move_up(self) -> None:
        """Move selection up (vim k key)."""
        focused = self.focused
        if focused and hasattr(focused, 'action_cursor_up'):
            focused.action_cursor_up()
    
    def action_add_feed(self) -> None:
        """Show add feed dialog."""
        self.run_worker(self._add_feed_worker(), exclusive=False)
    
    async def _add_feed_worker(self) -> None:
        """Worker to show add feed dialog."""
        result = await self.push_screen_wait(AddFeedDialog())
        
        if result:
            url, name = result
            try:
                feed_id = add_feed(url, name)
                self.notify(f"Added feed: {name}", timeout=5)
                
                # Refresh feed list
                feed_list = self.query_one("#feed-list", FeedList)
                feed_list.refresh_feeds()
            except Exception as e:
                self.notify(f"Error adding feed: {e}", severity="error", timeout=10)
    
    def action_delete_feed(self) -> None:
        """Delete selected feed."""
        self.run_worker(self._delete_feed_worker(), exclusive=False)
    
    async def _delete_feed_worker(self) -> None:
        """Worker to show delete confirmation dialog."""
        feed_list = self.query_one("#feed-list", FeedList)
        
        if feed_list.selected_feed_id is None:
            self.notify("No feed selected", severity="warning", timeout=3)
            return
        
        # Get feed name for confirmation
        feeds = get_all_feeds()
        feed = next((f for f in feeds if f['feed_id'] == feed_list.selected_feed_id), None)
        if not feed:
            return
        
        confirmed = await self.push_screen_wait(ConfirmDeleteDialog(feed['name']))
        
        if confirmed:
            try:
                delete_feed(feed_list.selected_feed_id)
                self.notify(f"Deleted feed: {feed['name']}", timeout=5)
                
                # Refresh UI
                feed_list.refresh_feeds()
                article_list = self.query_one("#article-list", ArticleList)
                article_list.load_articles(0)  # Clear articles
            except Exception as e:
                self.notify(f"Error deleting feed: {e}", severity="error", timeout=10)
    
    def action_toggle_like(self) -> None:
        """Like/unlike current article."""
        reader = self.query_one("#article-reader", ArticleReader)
        
        if reader.current_article_id is None:
            self.notify("No article selected", severity="warning", timeout=3)
            return
        
        # Check if already liked
        liked_articles = get_liked_articles()
        is_liked = any(a['article_id'] == reader.current_article_id for a in liked_articles)
        
        try:
            if is_liked:
                unlike_article(reader.current_article_id)
                self.notify("Article unliked", timeout=3)
            else:
                like_article(reader.current_article_id)
                self.notify("Article liked ♥", timeout=3)
            
            # Refresh reader and article list to show heart
            reader.refresh_article()
            article_list = self.query_one("#article-list", ArticleList)
            article_list.refresh_articles()
        except Exception as e:
            self.notify(f"Error toggling like: {e}", severity="error", timeout=10)
    
    def action_update_feeds(self) -> None:
        """Update all feeds in background."""
        feeds = get_all_feeds()
        
        if not feeds:
            self.notify("No feeds to update. Press 'a' to add one.", severity="warning", timeout=5)
            return
        
        self.notify(f"Updating {len(feeds)} feeds...", timeout=3)
        # Pass the callable as a worker with feeds as a parameter
        from functools import partial
        self.run_worker(partial(self._update_feeds_worker, feeds), exclusive=True, thread=True)
    
    def _update_feeds_worker(self, feeds: list) -> None:
        """Worker to update feeds in background thread."""
        total_new = 0
        errors = []
        
        for feed in feeds:
            try:
                new_count = fetch_and_store_feed(feed['feed_id'])
                total_new += new_count
                logger.info(f"Updated {feed['name']}: {new_count} new articles")
            except FeedFetchError as e:
                logger.error(f"Failed to update {feed['name']}: {e}")
                errors.append(feed['name'])
            except Exception as e:
                logger.error(f"Unexpected error updating {feed['name']}: {e}")
                errors.append(feed['name'])
        
        # Refresh UI on main thread
        self.call_from_thread(self._after_update, total_new, len(feeds), errors)
    
    def _after_update(self, total_new: int, total_feeds: int, errors: list) -> None:
        """Called after update completes to refresh UI."""
        # Refresh all widgets
        feed_list = self.query_one("#feed-list", FeedList)
        feed_list.refresh_feeds()
        
        article_list = self.query_one("#article-list", ArticleList)
        article_list.refresh_articles()
        
        # Show notification
        if errors:
            self.notify(
                f"Updated {total_feeds - len(errors)}/{total_feeds} feeds. "
                f"Added {total_new} articles. {len(errors)} failed.",
                severity="warning",
                timeout=8
            )
        else:
            self.notify(f"Updated {total_feeds} feeds. Added {total_new} new articles.", timeout=5)
    
    def action_recommendations(self) -> None:
        """Show recommendations (placeholder for Phase 3)."""
        self.run_worker(self._get_recommendations_worker, exclusive=False)
    
    async def _get_recommendations_worker(self) -> None:
        """Worker to generate and display recommendations."""
        try:
            from ..ml import get_recommendations
            
            # Show loading notification
            self.notify("Generating recommendations...", timeout=2)
            
            # Get recommendations
            recommendations = get_recommendations(user_id=1, limit=20)
            
            if not recommendations:
                # Check if user has enough liked articles
                from ..db import get_liked_articles
                liked = get_liked_articles()
                if len(liked) < 5:
                    self.notify(
                        f"Like at least 5 articles to get recommendations (you have {len(liked)})",
                        severity="warning",
                        timeout=5
                    )
                else:
                    self.notify("No recommendations available", timeout=3)
                return
            
            # For MVP, show recommendations in a simple notification
            # In future, could create a dedicated recommendations screen
            top_5 = recommendations[:5]
            message = "Top Recommendations:\n" + "\n".join([
                f"  • {r['title'][:50]}... ({r['similarity_score']:.2f})"
                for r in top_5
            ])
            
            self.notify(message, timeout=10)
            logger.info(f"Generated {len(recommendations)} recommendations")
            
        except ImportError:
            self.notify(
                "ML features not available. Install: pip install sentence-transformers scikit-learn",
                severity="error",
                timeout=10
            )
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}", exc_info=True)
            self.notify(f"Error generating recommendations: {e}", severity="error", timeout=8)


def main() -> None:
    """Entry point for RSS Reader TUI."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
        filename='rss_reader.log'
    )
    
    app = RSSReaderApp()
    app.run()


if __name__ == "__main__":
    main()
