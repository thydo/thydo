#!/usr/bin/env python3
"""
Resume Sync Script

Syncs resume assets from markdown frontmatter files in resume/sections/.

Generates:
  - resume_content.md - Markdown formatted resume
  - text_content.txt - Plain text resume
  - src/components/README.md - Component documentation

Usage:
  python -m resume.scripts.sync        # Normal output
  python -m resume.scripts.sync -q     # Quiet mode (only on changes)
"""

import argparse
import difflib
import sys
from datetime import datetime
from pathlib import Path

import frontmatter

from .config import SECTIONS_DIR, MD_FILE, TXT_FILE, COMPONENTS_README, LOG_FILE
from .logger import Logger
from .render import generate_markdown, generate_plaintext, generate_readme


def load_section(section_dir: Path) -> dict | None:
    """Load a section from its directory."""
    files = sorted(section_dir.glob('*.md'))
    header_file = next((f for f in files if f.name.startswith('00-')), None)

    if not header_file:
        return None

    with open(header_file) as f:
        header = frontmatter.load(f)

    section = {
        'type': header.get('type', 'plaintext'),
        'title': header.get('title', ''),
        'fields': header.get('fields', {}),
        'render_as_categories': header.get('render_as_categories', False),
        'items': []
    }

    for item_file in files:
        if item_file.name.startswith('00-'):
            continue
        with open(item_file) as f:
            item = frontmatter.load(f)
        item_data = dict(item.metadata)
        if item.content.strip():
            item_data['_content'] = item.content.strip()
        section['items'].append(item_data)

    return section


def load_resume_data() -> dict:
    """Load resume data from all section directories."""
    sections = []
    for section_dir in sorted(SECTIONS_DIR.iterdir()):
        if section_dir.is_dir():
            section = load_section(section_dir)
            if section:
                sections.append(section)
    return {'sections': sections}


def show_diff(old: str, new: str, filename: str) -> bool:
    """Display unified diff. Returns True if there are changes."""
    if old == new:
        return False

    diff = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=f'a/{filename}',
        tofile=f'b/{filename}'
    )
    print(f"\nChanges to {filename}:")
    print(''.join(diff))
    return True


def write_if_changed(path: Path, content: str) -> bool:
    """Write file only if content changed. Returns True if written."""
    old = path.read_text() if path.exists() else ''
    if old == content:
        return False
    path.write_text(content)
    return True


def sync(quiet: bool = False):
    """Sync all resume formats from frontmatter source files."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = load_resume_data()

    # Generate content
    outputs = [
        (MD_FILE, generate_markdown(data)),
        (TXT_FILE, generate_plaintext(data)),
        (COMPONENTS_README, generate_readme(data)),
    ]

    # Check for changes before writing
    changes = []
    for path, content in outputs:
        old = path.read_text() if path.exists() else ''
        if old != content:
            changes.append((path, old, content))
            path.write_text(content)

    if quiet:
        if changes:
            print(f"[{timestamp}] Synced ({len(changes)} file(s) changed)")
            for path, old, new in changes:
                show_diff(old, new, path.name)
    else:
        print(f"\nResume Sync - {timestamp}")
        print(f"Loaded {len(data['sections'])} sections")
        if changes:
            for path, old, new in changes:
                show_diff(old, new, path.name)
            print(f"\nUpdated: {', '.join(p.name for p, _, _ in changes)}")
        else:
            print("No changes detected")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Sync resume assets')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Quiet mode - only output when changes detected')
    args = parser.parse_args()

    if not SECTIONS_DIR.exists():
        print(f"Error: {SECTIONS_DIR} not found!", file=sys.stderr)
        return 1

    # Use logger to track updates (unless quiet mode)
    logger = None
    if not args.quiet:
        logger = Logger(LOG_FILE)
        sys.stdout = logger

    try:
        sync(quiet=args.quiet)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    finally:
        if logger:
            logger.save_log()
            sys.stdout = logger.terminal


if __name__ == "__main__":
    sys.exit(main())
