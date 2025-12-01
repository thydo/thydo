"""
Render functions for resume sync script.
Converts resume data to markdown and plain text formats.
"""

from .config import FIELD_STYLES


def get_field_type(field_name, fields_config):
    """Get the field type from the fields config."""
    field_def = fields_config.get(field_name)
    if isinstance(field_def, str):
        return field_def
    elif isinstance(field_def, dict):
        return field_def.get('type')
    return None


def get_field_prefix(field_name, fields_config, format='md'):
    """Get field-specific prefix, falling back to universal style."""
    field_def = fields_config.get(field_name)
    field_type = get_field_type(field_name, fields_config)

    # Check for field-specific prefix first
    if isinstance(field_def, dict):
        prefix = field_def.get(f'prefix_{format}') or field_def.get('prefix')
        if prefix:
            return prefix

    # Fall back to universal style
    style = FIELD_STYLES.get(field_type, {})
    return style.get(f'prefix_{format}', style.get('prefix_md', ''))


def get_field_suffix(field_name, fields_config, format='md'):
    """Get field-specific suffix, falling back to universal style."""
    field_def = fields_config.get(field_name)
    field_type = get_field_type(field_name, fields_config)

    # Check for field-specific suffix first
    if isinstance(field_def, dict):
        suffix = field_def.get(f'suffix_{format}') or field_def.get('suffix')
        if suffix:
            return suffix

    # Fall back to universal style
    style = FIELD_STYLES.get(field_type, {})
    return style.get(f'suffix_{format}', style.get('suffix_md', ''))


def render_section_markdown(section):
    """Render a single section to markdown format."""
    title = section.get('title', '')
    md = f"## {title}\n\n" if title else ""

    section_type = section.get('type', 'plaintext')
    fields_config = section.get('fields', {})
    items = section.get('items', [])

    # Plaintext sections - just render content
    if section_type == 'plaintext':
        for item in items:
            if '_content' in item:
                md += f"{item['_content']}\n\n"
        return md

    # Skills with categories rendering - uses first field in fields_config as category label
    # Resilient to field type changes (header, subheader, etc.)
    if section.get('render_as_categories'):
        category_field = next(iter(fields_config), None) if fields_config else None

        for item in items:
            if category_field and category_field in item:
                prefix = get_field_prefix(category_field, fields_config, 'md')
                suffix = get_field_suffix(category_field, fields_config, 'md')
                md += f"{prefix}{item[category_field]}:{suffix}\n"

            if '_content' in item:
                md += f"{item['_content']}\n\n"
        return md

    # Standard object items
    inline_sep = FIELD_STYLES.get('inline', {}).get('separator', ' | ')

    for item in items:
        # has_inline tracks whether we're currently accumulating inline fields on a single line.
        # Inline fields render on the same line separated by ' | ' (e.g., "May 2023 | GPA 3.5/4.0").
        # When we encounter a non-inline field, we need to close the inline line with a newline
        # before rendering the next field. We reset has_inline to False after adding that newline.
        has_inline = False

        for field_name in fields_config:
            if field_name not in item:
                continue

            field_type = get_field_type(field_name, fields_config)
            field_value = item[field_name]

            if field_type == 'header':
                prefix = get_field_prefix(field_name, fields_config, 'md')
                md += f"{prefix}{field_value}\n"

            elif field_type == 'inline':
                prefix = get_field_prefix(field_name, fields_config, 'md')
                md += f"{inline_sep if has_inline else ''}{prefix}{field_value}"
                has_inline = True  # Mark that we have an open inline line

            else:
                # Close any open inline line before rendering block-level fields
                if has_inline:
                    md += "\n"
                    has_inline = False

                if field_type == 'subheader':
                    prefix = get_field_prefix(field_name, fields_config, 'md')
                    suffix = get_field_suffix(field_name, fields_config, 'md')
                    md += f"{prefix}{field_value}{suffix}\n"

                elif field_type == 'list':
                    bullet = FIELD_STYLES.get('list', {}).get('bullet_md', '- ')
                    for list_item in field_value:
                        md += f"{bullet}{list_item}\n"

                else:
                    # Fallback for unknown/custom field types - render as plain text
                    prefix = get_field_prefix(field_name, fields_config, 'md')
                    suffix = get_field_suffix(field_name, fields_config, 'md')
                    md += f"{prefix}{field_value}{suffix}\n"

        # Close inline line if it was the last field in the item
        if has_inline:
            md += "\n"

        # Render content body (responsibilities, etc.)
        if '_content' in item:
            md += f"\n{item['_content']}\n"

        md += "\n"

    return md


def render_section_text(section):
    """Render a single section to plain text format."""
    title = section.get('title', '')
    txt = f"===== {title} =====\n" if title else ""

    section_type = section.get('type', 'plaintext')
    fields_config = section.get('fields', {})
    items = section.get('items', [])

    # Plaintext sections
    if section_type == 'plaintext':
        for item in items:
            if '_content' in item:
                txt += f"{item['_content']}\n\n"
        return txt

    # Skills with categories - uses first field in fields_config as category label
    # Resilient to field type changes (header, subheader, etc.)
    if section.get('render_as_categories'):
        category_field = next(iter(fields_config), None) if fields_config else None

        for item in items:
            if category_field and category_field in item:
                txt += f"{item[category_field]}:\n"

            if '_content' in item:
                txt += f"{item['_content']}\n\n"
        return txt

    # Standard object items
    inline_sep = FIELD_STYLES.get('inline', {}).get('separator', ' | ')

    for item in items:
        # has_inline tracks whether we're currently accumulating inline fields on a single line.
        # See render_section_markdown for detailed explanation.
        has_inline = False

        for field_name in fields_config:
            if field_name not in item:
                continue

            field_type = get_field_type(field_name, fields_config)
            field_value = item[field_name]

            if field_type == 'header':
                txt += f"{field_value}\n"

            elif field_type == 'inline':
                prefix = get_field_prefix(field_name, fields_config, 'txt')
                txt += f"{inline_sep if has_inline else ''}{prefix}{field_value}"
                has_inline = True  # Mark that we have an open inline line

            else:
                # Close any open inline line before rendering block-level fields
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
                    # Fallback for unknown/custom field types - render as plain text
                    prefix = get_field_prefix(field_name, fields_config, 'txt')
                    suffix = get_field_suffix(field_name, fields_config, 'txt')
                    txt += f"{prefix}{field_value}{suffix}\n"

        # Close inline line if it was the last field in the item
        if has_inline:
            txt += "\n"

        # Render content body
        if '_content' in item:
            txt += f"\n{item['_content']}\n"

        txt += "\n"

    return txt


def generate_markdown(data):
    """Generate complete markdown from resume data."""
    md = ""

    for section in data.get('sections', []):
        md += render_section_markdown(section)
        md += "---\n\n"

    return md


def generate_text(data):
    """Generate complete plain text from resume data."""
    txt = ""

    for section in data.get('sections', []):
        txt += render_section_text(section)

    return txt
