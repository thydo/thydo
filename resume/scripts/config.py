"""
Configuration for resume sync script.
Defines file paths and loads field type styling from config file.
"""

import os
import frontmatter

# File paths
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
RESUME_DIR = os.path.dirname(SCRIPTS_DIR)
PROJECT_ROOT = os.path.dirname(RESUME_DIR)
SECTIONS_DIR = os.path.join(RESUME_DIR, "sections")
CONFIG_FILE = os.path.join(RESUME_DIR, "00-config.md")

# Output files - resume folder
MD_FILE = os.path.join(RESUME_DIR, "resume_content.md")
TXT_FILE = os.path.join(RESUME_DIR, "text_content.txt")
JSON_FILE = os.path.join(RESUME_DIR, "resume_data.json")
LOG_FILE = os.path.join(SCRIPTS_DIR, "sync.log")

# Output files - Astro src folder
ASTRO_SRC_DIR = os.path.join(PROJECT_ROOT, "src")
ASTRO_DATA_DIR = os.path.join(ASTRO_SRC_DIR, "data")
ASTRO_SCHEMA_FILE = os.path.join(ASTRO_DATA_DIR, "resume-schema.ts")


def load_field_styles():
    """Load universal field type styling from config file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = frontmatter.load(f)
            return config.get('field_styles', {})
    return {}


FIELD_STYLES = load_field_styles()
