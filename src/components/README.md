# Components

Auto-generated from `resume/sections/`. Run `npm run sync` to update.

## Available Sections

| Component     | Title                   | Items |
|---------------|-------------------------|-------|
| 00-Personal   | (no title)              | 1     |
| 01-Plaintext  | SUMMARY                 | 1     |
| 02-Education  | EDUCATION               | 2     |
| 03-Skills     | TECHNICAL SKILLS        | 3     |
| 04-Experience | PROFESSIONAL EXPERIENCE | 6     |
| 05-Projects   | PROJECTS                | 3     |

## Structure

```
src/
├── layouts/
│   └── Layout.astro      # HTML shell (imports global.css, includes ProgressNav)
├── styles/
│   └── global.css        # CSS variables, reset, shared styles
├── utils/
│   ├── resume.ts         # Resume content utilities (getResumeItems, renderContent)
│   └── index.ts          # Barrel export
├── components/
│   ├── Header.astro      # HTML <head> content
│   ├── ProgressNav.astro # Scroll progress bar
│   ├── Footer.astro      # Site footer
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
    └── index.astro       # Page composition (layout grid, section order)
```

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
import { getResumeItems } from "../../utils";

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

This updates the markdown/text outputs and regenerates this README.

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
