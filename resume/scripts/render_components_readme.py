"""
Components README Generator

Generates a README.md in src/components/ listing available sections.
"""


def generate(data):
    """
    Generate components README with section structure.

    Args:
        data: Resume data with 'sections' list

    Returns:
        README content as string
    """
    sections = data.get('sections', [])

    rows = []
    for idx, section in enumerate(sections):
        section_type = section.get('type', 'unknown')
        title = section.get('title', '') or '(no title)'
        items = section.get('items', [])
        # Component name matches directory: 00-Personal, 01-Summary, etc.
        component = f"{idx:02d}-{section_type.title()}"
        rows.append((component, title, str(len(items))))

    # Calculate column widths (with minimums for visual alignment)
    col1_width = max(len(r[0]) for r in rows) if rows else 9
    col2_width = max(len(r[1]) for r in rows) if rows else 5
    col3_width = max(5, max(len(r[2]) for r in rows) if rows else 5)  # min 5 for "Items"

    # Build padded table
    header = f"| {'Component'.ljust(col1_width)} | {'Title'.ljust(col2_width)} | {'Items'.ljust(col3_width)} |"
    separator = f"|{'-' * (col1_width + 2)}|{'-' * (col2_width + 2)}|{'-' * (col3_width + 2)}|"
    section_lines = [f"| {r[0].ljust(col1_width)} | {r[1].ljust(col2_width)} | {r[2].ljust(col3_width)} |" for r in rows]

    sections_table = header + '\n' + separator + '\n' + '\n'.join(section_lines)

    readme = f'''# Components

Auto-generated from `resume/sections/`. Run `npm run sync` to update.

## Available Sections

{sections_table}

For structure, usage, adding new sections, CSS variables, and common patterns, see the main [README.md](../../README.md).
'''

    return readme
