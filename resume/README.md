# Resume Assets for Affinity Publisher

This directory contains all the assets you need to design and update your resume in Affinity Publisher.

## Directory Structure

```
resume/
├── 00-config.md              # Universal field type styling
├── sections/                 # Source content (edit these!)
│   ├── 00-personal/
│   ├── 01-summary/
│   ├── 02-education/
│   ├── 03-skills/
│   ├── 04-experience/
│   └── 05-projects/
├── resume_content.md         # Generated markdown (don't edit directly)
├── text_content.txt          # Generated plain text (don't edit directly)
└── scripts/
    └── sync.py               # Run to regenerate output files
```

## Editing Content

Edit files in `sections/` directories. Each section has:
- `00-*.md` - Section header defining type, title, and field mappings
- `01-*.md`, `02-*.md`, etc. - Individual items with frontmatter + content

### Example Item File
```yaml
---
position: Software Engineer
company: Acme Corp
duration: Jan 2024 - Present
---

- Built amazing things
- Delivered great results
```

After editing, run: `python3 -m scripts.sync`

## Field Types

Define field types in `00-*.md` section headers:

| Type | Markdown Output | Use For |
|------|-----------------|---------|
| `header` | `### Value` | Main titles (position, degree) |
| `subheader` | `**Value**` | Secondary info (company, institution) |
| `inline` | `Value \| Value` | Same-line fields (date, GPA) |
| `list` | `- Item` | Bullet lists |

### Custom Field Types

The renderer is resilient to custom/unknown field types. Unknown types render as plain text with any configured prefix/suffix:

```yaml
# Simple - renders as plain text
duration: custom_type

# With styling - applies prefix/suffix
duration:
  type: my_emphasis
  prefix_md: "_"
  suffix_md: "_"
```

### Universal Styling

Edit `00-config.md` to change default styling for all field types:

```yaml
field_styles:
  header:
    prefix_md: "### "
  subheader:
    prefix_md: "**"
    suffix_md: "**"
```

## Output Files

- **text_content.txt** - Plain text for copy-paste into Affinity Publisher
- **resume_content.md** - Markdown formatted version

## Color Palette
- **Primary Teal**: #007A7A (headers and name)
- **Black**: #000000 (body text)
- **Dark Gray**: Dates and secondary info

## Tips for Affinity Publisher
- Use Master Pages for consistent header/footer
- Set up paragraph styles for each section type
- Use character styles for emphasized text
- Export as PDF/X-1a or PDF/X-4 for professional printing
