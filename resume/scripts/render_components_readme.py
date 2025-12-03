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

    # Calculate column widths
    col1_width = max(len(r[0]) for r in rows) if rows else 9
    col2_width = max(len(r[1]) for r in rows) if rows else 5
    col3_width = max(len(r[2]) for r in rows) if rows else 5

    # Build padded table
    header = f"| {'Component'.ljust(col1_width)} | {'Title'.ljust(col2_width)} | {'Items'.ljust(col3_width)} |"
    separator = f"|{'-' * (col1_width + 2)}|{'-' * (col2_width + 2)}|{'-' * (col3_width + 2)}|"
    section_lines = [f"| {r[0].ljust(col1_width)} | {r[1].ljust(col2_width)} | {r[2].ljust(col3_width)} |" for r in rows]

    sections_table = header + '\n' + separator + '\n' + '\n'.join(section_lines)

    readme = f'''# Components

Auto-generated from `resume/sections/`. Run `npm run sync` to update.

## Available Sections

{sections_table}

## Structure

```
src/
├── layouts/
│   └── Layout.astro      # Page wrapper (imports global.css)
├── styles/
│   └── global.css        # CSS variables, reset, base styles
├── components/
│   ├── Header.astro      # HTML <head> content
│   ├── ProgressNav.astro # Scroll progress bar
│   ├── Footer.astro      # Site footer
│   ├── ResumeLayout.astro# Two-column layout
│   ├── index.ts          # Barrel export
│   └── sections/         # Resume section components
│       ├── 00-Personal.astro
│       ├── 01-Summary.astro
│       ├── 02-Education.astro
│       ├── 03-Skills.astro
│       ├── 04-Experience.astro
│       ├── 05-Projects.astro
│       └── index.ts      # Barrel export
└── pages/
    └── index.astro       # Main page
```

## Usage

```astro
import {{
  Personal,
  Education,
  Skills,
  Summary,
  Experience,
  Projects,
}} from "../components";
```

---

## Adding a New Section

### 1. Create resume content

Add a new folder in `resume/sections/` with numeric prefix for ordering:

```
resume/sections/06-certifications/
├── 00-certifications.md   # Section header
├── 01-aws.md              # First item
└── 02-gcp.md              # Second item
```

**Section header** (`00-certifications.md`):
```yaml
---
type: certifications
title: CERTIFICATIONS
fields:
  name: header
  issuer: subheader
  date: inline
---
```

**Item file** (`01-aws.md`):
```yaml
---
name: AWS Solutions Architect
issuer: Amazon Web Services
date: 2024
---
```

### 2. Create the Astro component

Create `src/components/sections/06-Certifications.astro`:

```astro
---
import {{ getCollection }} from "astro:content";

const allEntries = await getCollection("resume");
const items = allEntries
  .filter(e => e.id.startsWith("06-certifications/") && !e.id.includes("/00-"))
  .sort((a, b) => a.id.localeCompare(b.id));
---

<section id="certifications" class="section section--certifications">
  <h2>Certifications</h2>

  {{items.map((item) => (
    <article class="item">
      {{item.data.name && <h3>{{item.data.name}}</h3>}}
      <div class="item-meta">
        <div class="item-meta-left">
          {{item.data.issuer && <span class="subheader">{{item.data.issuer}}</span>}}
        </div>
        <div class="item-meta-right">
          {{item.data.date && <span>{{item.data.date}}</span>}}
        </div>
      </div>
    </article>
  ))}}
</section>

<style is:global>
  /* Add section-specific styles here */
  .section--certifications {{
    /* Custom styles */
  }}
</style>
```

### 3. Export the component

Add to `src/components/sections/index.ts`:
```ts
export {{ default as Certifications }} from "./06-Certifications.astro";
```

### 4. Add to page layout

Edit `src/pages/index.astro`:
```astro
import {{ Certifications }} from "../components";

// Add to sidebar or main content:
<ResumeLayout>
  <Fragment slot="main">
    <Certifications />
  </Fragment>
</ResumeLayout>
```

### 5. Update progress nav (optional)

If the section should appear in the progress bar, edit `src/components/ProgressNav.astro` to add nodes.

### 6. Run sync

```bash
npm run sync
```

This updates the markdown/text outputs and regenerates this README.

## CSS Variables

Available theme variables (defined in `src/styles/global.css`):

| Variable | Description |
|----------|-------------|
| `--h1` | Primary heading color |
| `--h2` | Section heading color |
| `--h3` | Item heading color |
| `--h4` | Subheading color |
| `--text` | Body text color |
| `--text-secondary` | Secondary/muted text |
| `--bg` | Background color |
| `--highlight` | Highlight animation color |
| `--border` | Border color |
| `--accent` | Accent/link color |
| `--size-h1` through `--size-sm` | Font sizes |
| `--section-gap`, `--item-gap` | Spacing |

## Common Patterns

**Section with items:**
```astro
<section class="section section--{{type}}">
  <h2>Title</h2>
  {{items.map(item => <article class="item">...</article>)}}
</section>
```

**Sidebar compact item:**
```astro
<article class="item item--compact">
  <h3>{{item.data.title}}</h3>
  <p class="subheader">{{item.data.subtitle}}</p>
  <p class="inline-info">{{item.data.detail}}</p>
</article>
```

**Main content item with meta:**
```astro
<article class="item">
  <h3>{{item.data.title}}</h3>
  <div class="item-meta">
    <div class="item-meta-left">
      <span class="subheader">{{item.data.company}}</span>
    </div>
    <div class="item-meta-right">
      <span>{{item.data.duration}}</span>
    </div>
  </div>
  <div class="content" set:html={{renderContent(item.body)}} />
</article>
```
'''

    return readme
