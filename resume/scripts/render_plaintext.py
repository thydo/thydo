"""
Plain Text Renderer for Resume Sync

Converts structured resume data into plain text format.
Used for generating text_content.txt for ATS systems, copy-paste, etc.

This is a stripped-down version of the markdown renderer:
  - No markdown formatting (**, ##, etc.)
  - Section headers use ===== TITLE ===== format
  - Bullets use • instead of -
  - Cleaner for text-only contexts

Field Types (same as markdown):
  - header:    Plain text on its own line
  - subheader: Plain text on its own line
  - inline:    Same line, separated by ' | '
  - list:      Bullet points with •
"""

from .config import FIELD_STYLES


def get_field_type(field_name, fields_config):
    """
    Extract field type from fields config.
    See render_markdown.py for detailed explanation.
    """
    field_def = fields_config.get(field_name)
    if isinstance(field_def, str):
        return field_def
    elif isinstance(field_def, dict):
        return field_def.get('type')
    return None


def get_field_prefix(field_name, fields_config):
    """
    Get plain text prefix for a field.

    Priority:
      1. Field-specific prefix_txt
      2. Field-specific prefix
      3. Universal style prefix_txt from FIELD_STYLES
    """
    field_def = fields_config.get(field_name)
    field_type = get_field_type(field_name, fields_config)

    if isinstance(field_def, dict):
        prefix = field_def.get('prefix_txt') or field_def.get('prefix')
        if prefix:
            return prefix

    style = FIELD_STYLES.get(field_type, {})
    return style.get('prefix_txt', '')


def get_field_suffix(field_name, fields_config):
    """
    Get plain text suffix for a field.
    Same priority as get_field_prefix but for suffixes.
    """
    field_def = fields_config.get(field_name)
    field_type = get_field_type(field_name, fields_config)

    if isinstance(field_def, dict):
        suffix = field_def.get('suffix_txt') or field_def.get('suffix')
        if suffix:
            return suffix

    style = FIELD_STYLES.get(field_type, {})
    return style.get('suffix_txt', '')


def render_section(section):
    """
    Render a single section to plain text format.

    Same logic as markdown renderer but:
      - Uses ===== TITLE ===== for headers
      - No markdown formatting in output
      - Uses • bullets instead of -
    """
    title = section.get('title', '')
    txt = f"===== {title} =====\n" if title else ""

    section_type = section.get('type', 'plaintext')
    fields_config = section.get('fields', {})
    items = section.get('items', [])

    # --- Plaintext sections ---
    if section_type == 'plaintext':
        for item in items:
            if '_content' in item:
                txt += f"{item['_content']}\n\n"
        return txt

    # --- Skills with categories ---
    if section.get('render_as_categories'):
        category_field = next(iter(fields_config), None) if fields_config else None

        for item in items:
            if category_field and category_field in item:
                txt += f"{item[category_field]}:\n"

            if '_content' in item:
                txt += f"{item['_content']}\n\n"
        return txt

    # --- Standard structured items ---
    inline_sep = FIELD_STYLES.get('inline', {}).get('separator', ' | ')

    for item in items:
        has_inline = False

        for field_name in fields_config:
            if field_name not in item:
                continue

            field_type = get_field_type(field_name, fields_config)
            field_value = item[field_name]

            if field_type == 'header':
                txt += f"{field_value}\n"

            elif field_type == 'inline':
                prefix = get_field_prefix(field_name, fields_config)
                txt += f"{inline_sep if has_inline else ''}{prefix}{field_value}"
                has_inline = True

            else:
                if has_inline:
                    txt += "\n"
                    has_inline = False

                if field_type == 'subheader':
                    txt += f"{field_value}\n"

                elif field_type == 'list':
                    bullet = FIELD_STYLES.get('list', {}).get('bullet_txt', '• ')
                    for list_item in field_value:
                        txt += f"{bullet}{list_item}\n"

                else:
                    prefix = get_field_prefix(field_name, fields_config)
                    suffix = get_field_suffix(field_name, fields_config)
                    txt += f"{prefix}{field_value}{suffix}\n"

        if has_inline:
            txt += "\n"

        if '_content' in item:
            txt += f"\n{item['_content']}\n"

        txt += "\n"

    return txt


def generate(data):
    """
    Generate complete plain text document from resume data.

    Args:
        data: Dict with 'sections' list from load_resume_data()

    Returns:
        Plain text string with all sections
    """
    txt = ""

    for section in data.get('sections', []):
        txt += render_section(section)

    return txt
