# Resume Content

Resume content managed as markdown files with YAML frontmatter. Powers both the Astro website and generates markdown/text outputs.

## Directory Structure

```
resume/
├── 00-config.md              # Field type styling for markdown/text renderers
├── sections/                 # Source content (edit these!)
│   ├── 00-personal/
│   ├── 01-summary/
│   ├── 02-education/
│   ├── 03-skills/
│   ├── 04-experience/
│   └── 05-projects/
├── resume_content.md         # Generated markdown
├── text_content.txt          # Generated plain text
└── scripts/
    └── sync.py               # Generates markdown + text outputs
```

## Editing Content

Edit files in `sections/` directories. Each section has:
- `00-*.md` - Section header defining type, title, and field mappings
- `01-*.md`, `02-*.md`, etc. - Individual items with frontmatter + content

After editing, run: `npm run sync`

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

## Field Types

| Type | Markdown Output | Use For |
|------|-----------------|---------|
| `header` | `### Value` | Main titles (position, degree) |
| `subheader` | `**Value**` | Secondary info (company, institution) |
| `inline` | `Value \| Value` | Same-line fields (date, GPA) |

## Output Files

- **resume_content.md** - Markdown formatted version
- **text_content.txt** - Plain text for copy-paste
