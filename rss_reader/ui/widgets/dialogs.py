"""Modal dialogs for feed management."""

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Label, Static
from textual.containers import Container, Horizontal, Vertical


class AddFeedDialog(ModalScreen[tuple[str, str] | None]):
    """Modal dialog for adding a new feed."""
    
    def compose(self) -> ComposeResult:
        """Create dialog layout."""
        yield Container(
            Vertical(
                Label("Add New Feed", id="dialog-title"),
                Label("URL:", classes="label"),
                Input(placeholder="https://example.com/feed.xml", id="url-input"),
                Label("Name:", classes="label"),
                Input(placeholder="My Feed", id="name-input"),
                Horizontal(
                    Button("Add", variant="primary", id="add-button"),
                    Button("Cancel", variant="default", id="cancel-button"),
                    classes="button-row"
                ),
                Label("", id="error-message", classes="error"),
                id="dialog-content"
            ),
            id="dialog-container"
        )
    
    def on_mount(self) -> None:
        """Focus URL input when dialog opens."""
        self.query_one("#url-input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        if event.button.id == "cancel-button":
            self.dismiss(None)
        elif event.button.id == "add-button":
            url = self.query_one("#url-input", Input).value
            name = self.query_one("#name-input", Input).value
            
            # Validate inputs
            if not url or not url.startswith(('http://', 'https://')):
                self.query_one("#error-message", Label).update(
                    "[red]Please enter a valid URL starting with http:// or https://[/red]"
                )
                return
            
            if not name:
                self.query_one("#error-message", Label).update(
                    "[red]Please enter a feed name[/red]"
                )
                return
            
            self.dismiss((url, name))


class ConfirmDeleteDialog(ModalScreen[bool]):
    """Modal dialog for confirming feed deletion."""
    
    def __init__(self, feed_name: str) -> None:
        self.feed_name = feed_name
        super().__init__()
    
    def compose(self) -> ComposeResult:
        """Create dialog layout."""
        yield Container(
            Vertical(
                Label("Confirm Delete", id="dialog-title"),
                Label(f"Delete feed '{self.feed_name}' and all its articles?"),
                Horizontal(
                    Button("Delete", variant="error", id="delete-button"),
                    Button("Cancel", variant="default", id="cancel-button"),
                    classes="button-row"
                ),
                id="dialog-content"
            ),
            id="dialog-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        if event.button.id == "cancel-button":
            self.dismiss(False)
        elif event.button.id == "delete-button":
            self.dismiss(True)
