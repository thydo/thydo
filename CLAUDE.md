# Claude Code Instructions

Project-specific instructions for Claude Code (Clawdie 🦀).

## Identity

Always sign commits and co-authorship as: `Clawdie 🦀 <noreply@anthropic.com>`

## Project Context

This is a resume website built with Astro. Resume content lives in `resume/sections/` as markdown files and gets synced to Astro components via `npm run sync`.

## Key Conventions

- **CSS**: Use CSS variables from `global.css`. Run `npm run lint:css` to check for hardcoded values.
- **Styles**: Use scoped `<style>` in components. Only use `is:global` when absolutely necessary, and prefer `global.css` for shared styles.
- **Utils**: Use `getResumeItems`, `getItemName`, `renderContent` from `src/utils` for resume data.
- **Sync**: Run `npm run sync` after modifying resume content or the README template.
