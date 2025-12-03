### Howdy 😃

✨ I'm Thy (pronounced `thee`)

💼 **Information Systems Engineer** at **TIAA** - Cloud Infrastructure & Automation

🌱 Expertise in **VMware Automation**, **Full-Stack Development**, and **UI/UX Design**

🎓 **Master of Science in Computer Science** from [**Arizona State University**](https://scai.engineering.asu.edu/)

📫 [LinkedIn](https://www.linkedin.com/in/thy-do) | [GitHub](https://github.com/thydo) | [thy.n.o.do@gmail.com](mailto:thy.n.o.do@gmail.com)

---

### This Repo

Personal website and resume at [thydo.github.io/thydo](https://thydo.github.io/thydo/) built with [Astro](https://astro.build/). Content lives in `resume/sections/` as markdown with YAML frontmatter.

```
thydo/
├── src/                    # Astro site
│   ├── layouts/            # Layout.astro - base template, CSS variables, global styles
│   ├── pages/              # index.astro - main page, content rendering, progress bar
│   ├── data/               # resume-schema.ts - generated TypeScript schema & theme
│   └── content.config.ts   # Astro content collection config
├── resume/                 # Resume content & sync scripts
│   ├── sections/           # Source content (edit these!)
│   ├── 00-config.md        # Theme & field styling config
│   └── scripts/            # Python renderers (markdown, plaintext, astro schema)
└── .github/                # GitHub Pages deployment
```

**Dev:** `npm run dev`
**Build:** `npm run build`
**Sync:** `python3 -m resume.scripts.sync`

### Astro Files

| File                        | What it does                                                                          |
|-----------------------------|---------------------------------------------------------------------------------------|
| `src/layouts/Layout.astro`  | Base HTML template, CSS variables from theme config, global styles                    |
| `src/pages/index.astro`     | Main page - loads content collections, renders sections, scroll progress tracking JS  |
| `src/data/resume-schema.ts` | **Generated** - TypeScript types + theme object, imported by Layout/index             |
| `src/content.config.ts`     | Astro content collection config - points to `resume/sections/`                        |

### Resume Content

| File                 | What it does                                                            |
|----------------------|-------------------------------------------------------------------------|
| `resume/00-config.md`| Theme colors, fonts, spacing, borders - synced to `resume-schema.ts`   |
| `resume/sections/`   | Markdown files with YAML frontmatter - each folder is a section        |
| `resume/scripts/`    | Python renderers: `render_markdown.py`, `render_plaintext.py`, etc.    |

---

## Usage

```astro
import {
  Personal,
  Education,
  Skills,
  Summary,
  Experience,
  Projects,
} from "../components";
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
import { getResumeItems } from "../utils";

const items = await getResumeItems("06-certifications");
---

<section id="certifications" class="section section--certifications">
  <h2>Certifications</h2>

  {items.map((item) => (
    <article class="item">
      {item.data.name && <h3>{item.data.name}</h3>}
      <div class="item-meta">
        <div class="item-meta-left">
          {item.data.issuer && <span class="subheader">{item.data.issuer}</span>}
        </div>
        <div class="item-meta-right">
          {item.data.date && <span>{item.data.date}</span>}
        </div>
      </div>
    </article>
  ))}
</section>

<style>
  /* Component-scoped styles (Astro auto-scopes these) */
  .section--certifications {
    /* Custom styles */
  }
</style>
```

> **Note:** Use `<style>` (scoped) for component-specific styles. Only use `<style is:global>` when styles must apply outside the component — and prefer putting those in `global.css` instead.

### 3. Export the component

Add to `src/components/sections/index.ts`:
```ts
export { default as Certifications } from "./06-Certifications.astro";
```

### 4. Add to page layout

Edit `src/pages/index.astro`:
```astro
import { Certifications } from "../components";

// Add to sidebar or main content:
<aside class="sidebar">
  <Certifications />
</aside>
// or
<main class="main-content">
  <Certifications />
</main>
```

### 5. Update progress nav (optional)

If the section should appear in the progress bar, edit `src/components/ProgressNav.astro` to add nodes.

### 6. Run sync

```bash
npm run sync
```

---

## CSS Variables

Available theme variables (defined in `src/styles/global.css`):

| Variable                              | Description              |
|---------------------------------------|--------------------------|
| `--h1` through `--h4`                 | Heading colors           |
| `--text`, `--text-secondary`          | Body text colors         |
| `--bg`, `--highlight`, `--border`     | UI colors                |
| `--accent`                            | Link/accent color        |
| `--size-h1` through `--size-label`    | Font sizes               |
| `--space-xs` through `--space-3xl`    | Spacing scale            |
| `--tracking`, `--tracking-wide`       | Letter spacing           |
| `--leading`, `--leading-relaxed`      | Line height              |
| `--section-gap`, `--item-gap`         | Component spacing        |
| `--sidebar-width`, `--container-max`  | Layout widths            |
| `--radius`                            | Border radius            |
| `--border-header`, `--border-section` | Border styles            |

---

## Common Patterns

**Section with items:**
```astro
<section class="section section--{type}">
  <h2>Title</h2>
  {items.map(item => <article class="item">...</article>)}
</section>
```

**Sidebar compact item:**
```astro
<article class="item item--compact">
  <h3>{item.data.title}</h3>
  <p class="subheader">{item.data.subtitle}</p>
  <p class="inline-info">{item.data.detail}</p>
</article>
```

**Main content item with meta:**
```astro
<article class="item">
  <h3>{item.data.title}</h3>
  <div class="item-meta">
    <div class="item-meta-left">
      <span class="subheader">{item.data.company}</span>
    </div>
    <div class="item-meta-right">
      <span>{item.data.duration}</span>
    </div>
  </div>
  <div class="content" set:html={renderContent(item.body)} />
</article>
```

