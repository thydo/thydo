---
# Universal styling for field types
field_styles:
  header:
    prefix_md: "### "
  subheader:
    prefix_md: "**"
    suffix_md: "**"
  inline:
    separator: " | "
  list:
    bullet_md: "- "
    bullet_txt: "• "

# Theme configuration for Astro site
theme:
  colors:
    primary: "#007A7A"
    text: "#1a1a1a"
    text_secondary: "#555"
    background: "#fff"
    border: "#e5e5e5"

  fonts:
    family: '"Inter", -apple-system, BlinkMacSystemFont, sans-serif'
    size_base: "15px"
    size_h1: "2.5rem"
    size_h2: "1.25rem"
    size_h3: "1.05rem"
    size_small: "0.9rem"

  spacing:
    container_max_width: "800px"
    container_padding: "3rem 2rem"
    section_margin: "2rem"
    item_margin: "1.5rem"

  borders:
    header: "2px solid"
    section: "1px solid"
---
