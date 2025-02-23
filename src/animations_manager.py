"""
When Parth cli tool starts, it displays a welcome message that animation is managed by this class.
"""

import time
import pyfiglet
from src.utility import console


class AnimationManager:
    """Manages animation effects and timing for the CLI interface."""

    def __init__(self, skip_animations=False):
        self.skip_animations = skip_animations
        self.default_delay = 0.05
        self.typing_delay = 0.02

    def animate_text(self, text, style="bold green", delay=None):
        """Animates text typing with configurable style and delay."""
        if self.skip_animations:
            console.print(text, style=style)
            return

        delay = delay or self.typing_delay
        for char in text:
            console.print(char, end="", style=style)
            time.sleep(delay)
        console.print()

    def animate_ascii_art(self, text, font="roman", style="bold cyan", delay=None):
        """Animates ASCII art text with configurable font and style."""
        if self.skip_animations:
            ascii_art = pyfiglet.figlet_format(text, font=font)
            console.print(ascii_art, style=style, justify="center")
            return

        delay = delay or self.default_delay
        ascii_art = pyfiglet.figlet_format(text, font=font)
        for line in ascii_art.split("\n"):
            if line.strip():  # Only animate non-empty lines
                console.print(line, style=style, justify="center")
                time.sleep(delay)
