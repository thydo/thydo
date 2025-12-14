# Components

Auto-generated from `resume/sections/`. Run `npm run sync` to update.

## Section Components

Resume content sections in `sections/`:

| Component     | Title                   | Items |
|---------------|-------------------------|-------|
| 00-Personal   | (no title)              | 1     |
| 01-Plaintext  | SUMMARY                 | 1     |
| 02-Education  | EDUCATION               | 2     |
| 03-Skills     | TECHNICAL SKILLS        | 3     |
| 04-Experience | PROFESSIONAL EXPERIENCE | 6     |
| 05-Projects   | PROJECTS                | 3     |

## Layout Components

| Component       | Purpose                                              |
|-----------------|------------------------------------------------------|
| `Header.astro`  | `<head>` meta tags, fonts, SEO                       |
| `Footer.astro`  | Page footer with credits                             |
| `ProgressNav.astro` | Scroll progress bar with section navigation nodes |

## Utils

Helpers in `utils/resume.ts`:

| Function | Purpose |
|----------|---------|
| `getResumeItems(prefix)` | Get all items from a section (excludes header files) |
| `getItemName(entry)` | Extract item name from file path |
| `renderContent(content)` | Convert markdown content to HTML |

## Imports

```ts
// Section components
import { Personal, Summary, Education, Skills, Experience, Projects } from "../components";

// Layout components
import { Header, Footer, ProgressNav } from "../components";

// Utils
import { getResumeItems, getItemName, renderContent } from "../components/utils";
```

For adding new sections, CSS variables, and common patterns, see [README.md](../../README.md).
