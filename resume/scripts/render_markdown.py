"""
Markdown Renderer for Resume Sync

Converts structured resume data (from frontmatter files) into formatted Markdown.
Used for generating resume_content.md which can be converted to PDF or shared.

Field Types & Rendering:
  - header:    Rendered as plain text on its own line (job title, degree)
  - subheader: Rendered with prefix/suffix styling (company, institution)
  - inline:    Rendered on same line, separated by ' | ' (dates, GPA)
  - list:      Rendered as bullet points (responsibilities)

Special Section Types:
  - plaintext:  Content rendered directly (summary)
  - categories: Uses render_as_categories for skills grouping
"""

from .config import FIELD_STYLES


def get_field_type(field_name, fields_config):
    """
    Extract field type from fields config.

    Fields can be defined as:
      - String: "header" -> type is "header"
      - Dict: {"type": "inline", "prefix": "GPA "} -> type is "inline"
    """
    field_def = fields_config.get(field_name)
    if isinstance(field_def, str):
        return field_def
    elif isinstance(field_def, dict):
        return field_def.get('type')
    return None


def get_field_prefix(field_name, fields_config):
    """
    Get markdown prefix for a field.

    Priority:
      1. Field-specific prefix_md in field config
      2. Field-specific prefix in field config
      3. Universal style prefix_md from FIELD_STYLES
    """
    field_def = fields_config.get(field_name)
    field_type = get_field_type(field_name, fields_config)

    # Check for field-specific prefix first
    if isinstance(field_def, dict):
        prefix = field_def.get('prefix_md') or field_def.get('prefix')
        if prefix:
            return prefix

    # Fall back to universal style
    style = FIELD_STYLES.get(field_type, {})
    return style.get('prefix_md', '')


def get_field_suffix(field_name, fields_config):
    """
    Get markdown suffix for a field.

    Same priority as get_field_prefix but for suffixes.
    """
    field_def = fields_config.get(field_name)
    field_type = get_field_type(field_name, fields_config)

    # Check for field-specific suffix first
    if isinstance(field_def, dict):
        suffix = field_def.get('suffix_md') or field_def.get('suffix')
        if suffix:
            return suffix

    # Fall back to universal style
    style = FIELD_STYLES.get(field_type, {})
    return style.get('suffix_md', '')


def render_section(section):
    """
    Render a single section to markdown format.

    Handles three section types:
      1. Plaintext: Direct content rendering (summary)
      2. Categories: Skills with category labels
      3. Standard: Structured items with header/subheader/inline/content fields
    """
    title = section.get('title', '')
    md = f"## {title}\n\n" if title else ""

    section_type = section.get('type', 'plaintext')
    fields_config = section.get('fields', {})
    items = section.get('items', [])

    # --- Plaintext sections (summary) ---
    # Just render the raw content from each item
    if section_type == 'plaintext':
        for item in items:
            if '_content' in item:
                md += f"{item['_content']}\n\n"
        return md

    # --- Skills with categories ---
    # Uses first field as category label, content as skill list
    if section.get('render_as_categories'):
        category_field = next(iter(fields_config), None) if fields_config else None

        for item in items:
            if category_field and category_field in item:
                prefix = get_field_prefix(category_field, fields_config)
                suffix = get_field_suffix(category_field, fields_config)
                md += f"{prefix}{item[category_field]}:{suffix}\n"

            if '_content' in item:
                md += f"{item['_content']}\n\n"
        return md

    # --- Standard structured items (experience, projects, education) ---
    inline_sep = FIELD_STYLES.get('inline', {}).get('separator', ' | ')

    for item in items:
        # Track if we're accumulating inline fields on a single line.
        # Inline fields render together: "May 2023 | GPA 3.5/4.0"
        # When we hit a non-inline field, we close the line with \n
        has_inline = False

        # Process fields in config order to maintain consistent output
        for field_name in fields_config:
            if field_name not in item:
                continue

            field_type = get_field_type(field_name, fields_config)
            field_value = item[field_name]

            # Header: Job title, degree name, project title
            if field_type == 'header':
                prefix = get_field_prefix(field_name, fields_config)
                md += f"{prefix}{field_value}\n"

            # Inline: Dates, GPA, location - all on same line
            elif field_type == 'inline':
                prefix = get_field_prefix(field_name, fields_config)
                md += f"{inline_sep if has_inline else ''}{prefix}{field_value}"
                has_inline = True

            else:
                # Close any open inline line before block-level fields
                if has_inline:
                    md += "\n"
                    has_inline = False

                # Subheader: Company name, institution
                if field_type == 'subheader':
                    prefix = get_field_prefix(field_name, fields_config)
                    suffix = get_field_suffix(field_name, fields_config)
                    md += f"{prefix}{field_value}{suffix}\n"

                # List: Bullet points (responsibilities, achievements)
                elif field_type == 'list':
                    bullet = FIELD_STYLES.get('list', {}).get('bullet_md', '- ')
                    for list_item in field_value:
                        md += f"{bullet}{list_item}\n"

                # Unknown type: Render as plain text with prefix/suffix
                else:
                    prefix = get_field_prefix(field_name, fields_config)
                    suffix = get_field_suffix(field_name, fields_config)
                    md += f"{prefix}{field_value}{suffix}\n"

        # Close inline line if it was the last field
        if has_inline:
            md += "\n"

        # Content body (responsibilities, project details)
        if '_content' in item:
            md += f"\n{item['_content']}\n"

        md += "\n"

    return md


def generate(data):
    """
    Generate complete markdown document from resume data.

    Args:
        data: Dict with 'sections' list from load_resume_data()

    Returns:
        Complete markdown string with all sections separated by ---
    """
    md = ""

    for section in data.get('sections', []):
        md += render_section(section)
        md += "---\n\n"

    return md
