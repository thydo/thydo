"""
Resume Renderer

Converts structured resume data into markdown or plain text format.
Consolidates render_markdown.py and render_plaintext.py into a single module.

Field Types:
  - header:    Main item title (job title, degree, project name)
  - subheader: Secondary info (company, institution)
  - inline:    Same line, separated by ' | ' (dates, GPA, location)
  - list:      Bullet points (responsibilities)

Section Types:
  - plaintext:  Content rendered directly (summary)
  - categories: Skills with category labels
  - (default):  Structured items with fields
"""

from .config import FIELD_STYLES

# Format-specific configuration
FORMAT_CONFIG = {
    'md': {
        'section_title': lambda t: f"## {t}\n\n",
        'section_sep': "---\n\n",
        'prefix_key': 'prefix_md',
        'suffix_key': 'suffix_md',
        'bullet_key': 'bullet_md',
        'default_bullet': '- ',
    },
    'txt': {
        'section_title': lambda t: f"===== {t} =====\n",
        'section_sep': "",
        'prefix_key': 'prefix_txt',
        'suffix_key': 'suffix_txt',
        'bullet_key': 'bullet_txt',
        'default_bullet': '• ',
    },
}


def get_field_type(field_name, fields_config):
    """Extract field type from fields config (string or dict with 'type' key)."""
    field_def = fields_config.get(field_name)
    if isinstance(field_def, str):
        return field_def
    if isinstance(field_def, dict):
        return field_def.get('type')
    return None


def get_field_affix(field_name, fields_config, fmt, affix_type):
    """
    Get prefix or suffix for a field.

    Priority:
      1. Field-specific format affix (prefix_md/suffix_md or prefix_txt/suffix_txt)
      2. Field-specific generic affix (prefix/suffix)
      3. Universal style affix from FIELD_STYLES
    """
    field_def = fields_config.get(field_name)
    field_type = get_field_type(field_name, fields_config)
    config = FORMAT_CONFIG[fmt]
    affix_key = config[f'{affix_type}_key']

    if isinstance(field_def, dict):
        # Try format-specific, then generic
        affix = field_def.get(affix_key) or field_def.get(affix_type)
        if affix:
            return affix

    # Fall back to universal style
    style = FIELD_STYLES.get(field_type, {})
    return style.get(affix_key, '')


def render_section(section, fmt='md'):
    """Render a single section to the specified format."""
    config = FORMAT_CONFIG[fmt]
    title = section.get('title', '')
    output = config['section_title'](title) if title else ""

    section_type = section.get('type', 'plaintext')
    fields_config = section.get('fields', {})
    items = section.get('items', [])

    # Plaintext sections (summary) - just render content
    if section_type == 'plaintext':
        for item in items:
            if '_content' in item:
                output += f"{item['_content']}\n\n"
        return output

    # Skills with categories
    if section.get('render_as_categories'):
        category_field = next(iter(fields_config), None) if fields_config else None
        for item in items:
            if category_field and category_field in item:
                prefix = get_field_affix(category_field, fields_config, fmt, 'prefix')
                suffix = get_field_affix(category_field, fields_config, fmt, 'suffix')
                output += f"{prefix}{item[category_field]}:{suffix}\n"
            if '_content' in item:
                output += f"{item['_content']}\n\n"
        return output

    # Standard structured items (experience, education, projects)
    inline_sep = FIELD_STYLES.get('inline', {}).get('separator', ' | ')
    bullet = FIELD_STYLES.get('list', {}).get(config['bullet_key'], config['default_bullet'])

    for item in items:
        has_inline = False

        for field_name in fields_config:
            if field_name not in item:
                continue

            field_type = get_field_type(field_name, fields_config)
            field_value = item[field_name]

            if field_type == 'header':
                prefix = get_field_affix(field_name, fields_config, fmt, 'prefix')
                output += f"{prefix}{field_value}\n"

            elif field_type == 'inline':
                prefix = get_field_affix(field_name, fields_config, fmt, 'prefix')
                output += f"{inline_sep if has_inline else ''}{prefix}{field_value}"
                has_inline = True

            else:
                if has_inline:
                    output += "\n"
                    has_inline = False

                if field_type == 'subheader':
                    prefix = get_field_affix(field_name, fields_config, fmt, 'prefix')
                    suffix = get_field_affix(field_name, fields_config, fmt, 'suffix')
                    output += f"{prefix}{field_value}{suffix}\n"

                elif field_type == 'list':
                    for list_item in field_value:
                        output += f"{bullet}{list_item}\n"

                else:
                    prefix = get_field_affix(field_name, fields_config, fmt, 'prefix')
                    suffix = get_field_affix(field_name, fields_config, fmt, 'suffix')
                    output += f"{prefix}{field_value}{suffix}\n"

        if has_inline:
            output += "\n"

        if '_content' in item:
            output += f"\n{item['_content']}\n"

        output += "\n"

    return output


def generate(data, fmt='md'):
    """Generate complete document from resume data in specified format."""
    config = FORMAT_CONFIG[fmt]
    output = ""

    for section in data.get('sections', []):
        output += render_section(section, fmt)
        output += config['section_sep']

    return output


def generate_markdown(data):
    """Generate markdown document."""
    return generate(data, 'md')


def generate_plaintext(data):
    """Generate plain text document."""
    return generate(data, 'txt')


def generate_readme(data):
    """Generate components README with section structure."""
    sections = data.get('sections', [])

    rows = []
    for idx, section in enumerate(sections):
        section_type = section.get('type', 'unknown')
        title = section.get('title', '') or '(no title)'
        items = section.get('items', [])
        component = f"{idx:02d}-{section_type.title()}"
        rows.append((component, title, str(len(items))))

    if not rows:
        return "# Components\n\nNo sections found.\n"

    # Calculate column widths
    widths = [
        max(len(r[0]) for r in rows),
        max(len(r[1]) for r in rows),
        max(5, max(len(r[2]) for r in rows)),
    ]

    # Build table
    header = f"| {'Component'.ljust(widths[0])} | {'Title'.ljust(widths[1])} | {'Items'.ljust(widths[2])} |"
    sep = f"|{'-' * (widths[0] + 2)}|{'-' * (widths[1] + 2)}|{'-' * (widths[2] + 2)}|"
    lines = [f"| {r[0].ljust(widths[0])} | {r[1].ljust(widths[1])} | {r[2].ljust(widths[2])} |" for r in rows]

    return f'''# Components

Auto-generated from `resume/sections/`. Run `npm run sync` to update.

## Available Sections

{header}
{sep}
{chr(10).join(lines)}

For structure, usage, adding new sections, CSS variables, and common patterns, see the main [README.md](../../README.md).
'''
