"""
Logger class for resume sync script.
Writes to both console and log file, with most recent entries at top.
"""

import sys
from pathlib import Path


class Logger:
    """Logger that writes to both console and log file. Most recent entries at top."""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.terminal = sys.stdout
        self.buffer = []

    def write(self, message):
        """Write to terminal and buffer for log file."""
        self.terminal.write(message)
        self.buffer.append(message)

    def flush(self):
        """Flush terminal output."""
        self.terminal.flush()

    def save_log(self):
        """Prepend buffered content to log file (most recent at top)."""
        new_content = ''.join(self.buffer)
        if not new_content.strip():
            return

        existing = self.log_file.read_text() if self.log_file.exists() else ''
        self.log_file.write_text(new_content + existing)
