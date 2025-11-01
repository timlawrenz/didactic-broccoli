#!/usr/bin/env python3
"""Minimal test to check if we can display feeds."""

from textual.app import App, ComposeResult
from textual.widgets import Static, Label
from textual.containers import VerticalScroll

from rss_reader.db import get_all_feeds

class TestApp(App):
    def compose(self) -> ComposeResult:
        yield Label("Test Feed Display")
        yield VerticalScroll(id="test-container")
    
    def on_mount(self) -> None:
        container = self.query_one("#test-container", VerticalScroll)
        feeds = get_all_feeds()
        
        if not feeds:
            container.mount(Static("No feeds found"))
        else:
            for feed in feeds:
                container.mount(Static(f"Feed: {feed['name']}"))

if __name__ == "__main__":
    app = TestApp()
    app.run()
