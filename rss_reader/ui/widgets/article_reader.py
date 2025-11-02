"""Article reader widget for right panel."""

from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.containers import VerticalScroll
from textual.reactive import reactive

from ...db import get_liked_articles


class ArticleReader(Static):
    """Widget displaying full article content."""
    
    DEFAULT_CSS = """
    ArticleReader {
        width: 100%;
        height: 100%;
    }
    
    #reader-container {
        width: 100%;
        height: 1fr;
        overflow-x: hidden;
        overflow-y: auto;
    }
    
    #reader-content {
        width: 100%;
        height: auto;
        padding: 1;
    }
    """
    
    current_article_id: reactive[int | None] = reactive(None)
    current_article: reactive[dict | None] = reactive(None)
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Label("📖 Reader", id="reader-header")
        yield VerticalScroll(
            Static("[dim]Select an article to read[/dim]", id="reader-content"),
            id="reader-container"
        )
    
    def load_article(self, article_id: int, article: dict) -> None:
        """Load and display article content."""
        self.current_article_id = article_id
        self.current_article = article
        
        # Check if article is liked
        liked_articles = get_liked_articles()
        is_liked = any(a['article_id'] == article_id for a in liked_articles)
        
        # Format article content
        heart = "♥ Liked" if is_liked else ""
        date_str = article.get('published_date', 'Unknown date')
        if date_str and len(date_str) > 10:
            date_str = date_str[:10]
        
        content = f"""[bold]{article['title']}[/bold]

{heart}
[dim]Published: {date_str}[/dim]
[dim]Link: {article['link']}[/dim]

---

{article.get('full_text') or article.get('summary') or '[dim]No content available[/dim]'}
"""
        
        # Update reader content
        reader_content = self.query_one("#reader-content", Static)
        reader_content.update(content)
    
    def refresh_article(self) -> None:
        """Reload current article (to update liked status)."""
        if self.current_article_id and self.current_article:
            self.load_article(self.current_article_id, self.current_article)
