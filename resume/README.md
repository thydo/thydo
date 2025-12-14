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
    ├── sync.py               # Main entry - loads sections, generates outputs
    ├── render.py             # Renders to markdown, plaintext, and README
    ├── config.py             # Path configuration and field style loading
    └── logger.py             # Tracks content changes (prepends to sync.log)
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

## Sync Scripts

### Usage

```bash
# Normal sync - outputs to console and logs to sync.log
npm run sync
# or
python3 -m resume.scripts.sync

# Quiet mode - only outputs when changes detected (no logging)
npm run sync -- -q
# or
python3 -m resume.scripts.sync -q

# Watch mode - auto-syncs on file changes (used by npm run dev)
npm run watch:sync
```

### Output Files

| Output                       | Description                                      |
|------------------------------|--------------------------------------------------|
| `resume_content.md`          | Markdown resume (for PDF conversion)             |
| `text_content.txt`           | Plain text resume (for ATS systems)              |
| `../src/components/README.md`| Auto-generated component documentation           |
| `scripts/sync.log`           | Change history (latest at top, gitignored)       |
