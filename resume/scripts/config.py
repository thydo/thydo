"""
Configuration for resume sync script.
Defines file paths and loads field type styling from config file.
"""

from pathlib import Path

import frontmatter

# Paths
_SCRIPTS_DIR = Path(__file__).parent
RESUME_DIR = _SCRIPTS_DIR.parent
PROJECT_ROOT = RESUME_DIR.parent
SECTIONS_DIR = RESUME_DIR / "sections"

# Output files
MD_FILE = RESUME_DIR / "resume_content.md"
TXT_FILE = RESUME_DIR / "text_content.txt"
COMPONENTS_README = PROJECT_ROOT / "src" / "components" / "README.md"
LOG_FILE = _SCRIPTS_DIR / "sync.log"

# Load field styles from config
_CONFIG_FILE = RESUME_DIR / "00-config.md"
FIELD_STYLES = {}
if _CONFIG_FILE.exists():
    with open(_CONFIG_FILE) as f:
        FIELD_STYLES = frontmatter.load(f).get('field_styles', {})
