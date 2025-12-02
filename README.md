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

| File | What it does |
|------|--------------|
| `src/layouts/Layout.astro` | Base HTML template, CSS variables from theme config, global styles (typography, layout grid, progress bar) |
| `src/pages/index.astro` | Main page - loads content collections, renders sections, scroll progress tracking JS |
| `src/data/resume-schema.ts` | **Generated** - TypeScript types + theme object, imported by Layout/index |
| `src/content.config.ts` | Astro content collection config - points to `resume/sections/` |

### Resume Content

| File | What it does |
|------|--------------|
| `resume/00-config.md` | Theme colors, fonts, spacing, borders - synced to `resume-schema.ts` |
| `resume/sections/` | Markdown files with YAML frontmatter - each folder is a section |
| `resume/scripts/` | Python renderers: `render_markdown.py`, `render_plaintext.py`, `render_astro.py` |

