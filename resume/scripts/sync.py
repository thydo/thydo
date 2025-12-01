#!/usr/bin/env python3
"""
Resume Asset Synchronization Script
Main entry point for syncing resume assets from markdown frontmatter files.
"""

import difflib
import json
import os
import sys
from datetime import datetime

import frontmatter

from .config import (
    SECTIONS_DIR, MD_FILE, TXT_FILE, JSON_FILE, LOG_FILE,
    CONFIG_FILE, ASTRO_DATA_DIR, ASTRO_SCHEMA_FILE
)
from .logger import Logger
from .render import generate_markdown, generate_text, generate_astro_schema


def get_file_content(filepath):
    """Read file content or return empty string if file doesn't exist."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return ''


def show_diff(old_content, new_content, filename):
    """Display unified diff between old and new content."""
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff = list(difflib.unified_diff(old_lines, new_lines, fromfile=f'a/{filename}', tofile=f'b/{filename}'))

    if diff:
        print(f"\nChanges to {filename}:")
        print(''.join(diff))
    else:
        print(f"\nNo changes to {filename}")


def load_section(section_dir):
    """Load a section from its directory."""
    files = sorted(os.listdir(section_dir))

    # Find and load the header file (00-*.md)
    header_file = None
    item_files = []

    for f in files:
        if f.endswith('.md'):
            if f.startswith('00-'):
                header_file = f
            else:
                item_files.append(f)

    if not header_file:
        return None

    # Load header config
    header_path = os.path.join(section_dir, header_file)
    with open(header_path, 'r') as f:
        header = frontmatter.load(f)

    section = {
        'type': header.get('type', 'plaintext'),
        'title': header.get('title', ''),
        'fields': header.get('fields', {}),
        'render_as_categories': header.get('render_as_categories', False),
        'items': []
    }

    # Load item files
    for item_file in item_files:
        item_path = os.path.join(section_dir, item_file)
        with open(item_path, 'r') as f:
            item = frontmatter.load(f)

        # Build item dict from frontmatter
        item_data = dict(item.metadata)

        # Add content body if present (for responsibilities, lists, etc.)
        if item.content.strip():
            item_data['_content'] = item.content.strip()

        section['items'].append(item_data)

    return section


def load_resume_data():
    """Load resume data from frontmatter files."""
    sections = []

    # Get all section directories, sorted by numeric prefix
    section_dirs = sorted([
        d for d in os.listdir(SECTIONS_DIR)
        if os.path.isdir(os.path.join(SECTIONS_DIR, d))
    ])

    for section_dir_name in section_dirs:
        section_path = os.path.join(SECTIONS_DIR, section_dir_name)
        section = load_section(section_path)
        if section:
            sections.append(section)

    return {'sections': sections}


def load_theme_config():
    """Load theme configuration from 00-config.md."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = frontmatter.load(f)
            return dict(config.metadata)
    return {}


def sync_all(quiet=False):
    """Sync all resume formats from frontmatter source files."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Load data
        data = load_resume_data()
        theme_config = load_theme_config()

        # Capture old content for diff
        old_md = get_file_content(MD_FILE)
        old_txt = get_file_content(TXT_FILE)
        old_astro = get_file_content(ASTRO_SCHEMA_FILE)

        # Generate content
        md_content = generate_markdown(data)
        txt_content = generate_text(data)
        os.makedirs(ASTRO_DATA_DIR, exist_ok=True)
        astro_content = generate_astro_schema(data, theme_config)

        # Check if anything changed
        has_changes = (
            old_md != md_content or
            old_txt != txt_content or
            old_astro != astro_content
        )

        # Write files
        with open(MD_FILE, 'w') as f:
            f.write(md_content)
        with open(TXT_FILE, 'w') as f:
            f.write(txt_content)
        with open(ASTRO_SCHEMA_FILE, 'w') as f:
            f.write(astro_content)

        if quiet:
            if has_changes:
                print(f"[{timestamp}] ✓ Synced (changes detected)")
                show_diff(old_md, md_content, 'resume_content.md')
                show_diff(old_txt, txt_content, 'text_content.txt')
                show_diff(old_astro, astro_content, 'src/data/resume-schema.ts')
            # Silent when no changes in quiet mode
        else:
            print(f"\n{'='*60}")
            print(f"Resume Sync - {timestamp}")
            print(f"{'='*60}")
            print(f"✓ Loaded {len(data.get('sections', []))} sections")
            print(f"✓ Updated: resume_content.md, text_content.txt, resume-schema.ts")
            show_diff(old_md, md_content, 'resume_content.md')
            show_diff(old_txt, txt_content, 'text_content.txt')
            show_diff(old_astro, astro_content, 'src/data/resume-schema.ts')
            print(f"\n✅ All assets synchronized successfully!")
            print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n❌ Error during sync: {str(e)}")
        raise


def main():
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description='Sync resume assets')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Quiet mode - only output when changes detected')
    args = parser.parse_args()

    # Set up logging (skip in quiet mode)
    if not args.quiet:
        logger = Logger(LOG_FILE)
        sys.stdout = logger

    try:
        if not os.path.exists(SECTIONS_DIR):
            print(f"Error: {SECTIONS_DIR} not found!")
            return 1

        sync_all(quiet=args.quiet)
        return 0

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        if not args.quiet:
            # Save log (most recent at top) and restore stdout
            logger.save_log()
            sys.stdout = logger.terminal


if __name__ == "__main__":
    sys.exit(main())
