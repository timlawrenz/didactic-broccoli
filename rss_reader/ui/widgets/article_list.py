"""Article list widget for center panel."""

from textual.app import ComposeResult
from textual.widgets import Static, ListView, ListItem, Label
from textual.message import Message
from textual.reactive import reactive

from ...db import get_articles_by_feed, get_liked_articles


class ArticleList(Static):
    """Widget displaying articles from selected feed."""
    
    class ArticleSelected(Message):
        """Message sent when an article is selected."""
        
        def __init__(self, article_id: int, article: dict) -> None:
            self.article_id = article_id
            self.article = article
            super().__init__()
    
    current_feed_id: reactive[int | None] = reactive(None)
    selected_article_id: reactive[int | None] = reactive(None)
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Label("📰 Articles", id="article-header")
        yield ListView(id="article-listview")
    
    def load_articles(self, feed_id: int) -> None:
        """Load articles from database for given feed."""
        self.current_feed_id = feed_id
        listview = self.query_one("#article-listview", ListView)
        listview.clear()
        
        articles = get_articles_by_feed(feed_id, limit=100)
        
        if not articles:
            listview.append(ListItem(Label("[dim]No articles yet. Press 'u' to fetch.[/dim]")))
            return
        
        # Get liked articles for this user
        liked_articles = get_liked_articles()
        liked_ids = {a['article_id'] for a in liked_articles}
        
        for article in articles:
            # Format article info
            heart = "♥ " if article['article_id'] in liked_ids else ""
            date_str = ""
            if article['published_date']:
                date_str = f" [dim]{article['published_date'][:10]}[/dim]"
            
            label = Label(f"{heart}{article['title']}{date_str}")
            item = ListItem(label)
            item.article_id = article['article_id']
            item.article_data = dict(article)
            listview.append(item)
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle article selection."""
        if hasattr(event.item, 'article_id'):
            self.selected_article_id = event.item.article_id
            self.post_message(self.ArticleSelected(event.item.article_id, event.item.article_data))
    
    def refresh_articles(self) -> None:
        """Reload articles for current feed."""
        if self.current_feed_id is not None:
            self.load_articles(self.current_feed_id)
