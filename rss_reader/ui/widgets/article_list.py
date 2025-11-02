"""Article list widget for center panel."""

from textual.app import ComposeResult
from textual.widgets import Static, ListView, ListItem, Label
from textual.message import Message
from textual.reactive import reactive

from ...db import get_articles_by_feed, get_all_articles_sorted, get_liked_articles
from ...ml import get_recommendations


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
        
        # Check if this is "All Articles" (feed_id == 0)
        if feed_id == 0:
            articles = get_all_articles_sorted(limit=100)
        elif feed_id == -1:
            # Recommended feed
            liked_count = len(get_liked_articles())
            if liked_count < 5:
                listview.append(ListItem(Label(
                    f"[dim]Like at least 5 articles to see recommendations (you have {liked_count})[/dim]\n\n"
                    f"[dim]Try browsing 'All Articles' and liking content that interests you![/dim]"
                )))
                return
            
            try:
                articles = get_recommendations(limit=50)
                if not articles:
                    listview.append(ListItem(Label(
                        "[dim]No recommendations available[/dim]\n\n"
                        "[dim]Try adding more feeds or liking more articles.[/dim]"
                    )))
                    return
            except Exception as e:
                listview.append(ListItem(Label(
                    "[dim]Recommendations temporarily unavailable[/dim]\n\n"
                    f"[dim]Error: {e}[/dim]"
                )))
                return
        elif feed_id == -2:
            # Liked feed
            liked_articles = get_liked_articles()
            if not liked_articles:
                listview.append(ListItem(Label(
                    "[dim]No liked articles yet[/dim]\n\n"
                    "[dim]Press 'l' while reading articles to save them here.[/dim]\n"
                    "[dim]Liked articles are used for personalized recommendations.[/dim]"
                )))
                return
            
            # Sort by most recently liked (newest first)
            # Note: get_liked_articles() should already return liked_date
            articles = sorted(liked_articles, 
                             key=lambda x: x.get('liked_date', ''), 
                             reverse=True)
        else:
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
            
            # Add feed name prefix for "All Articles", "Recommended", and "Liked" views
            if (feed_id == 0 or feed_id == -1 or feed_id == -2) and 'feed_name' in article:
                title = f"[cyan]{article['feed_name']}[/cyan] {article['title']}"
            else:
                title = article['title']
            
            # Add similarity score for recommendations (optional)
            score_str = ""
            if feed_id == -1 and 'similarity_score' in article:
                score_pct = int(article['similarity_score'] * 100)
                score_str = f" [dim]({score_pct}%)[/dim]"
            
            label = Label(f"{heart}{title}{date_str}{score_str}")
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
