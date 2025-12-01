import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

export interface Theme {
  colors: {
    primary: string;
    text: string;
    text_secondary: string;
    background: string;
    border: string;
  };
  fonts: {
    family: string;
    size_base: string;
    size_h1: string;
    size_h2: string;
    size_h3: string;
    size_small: string;
  };
  spacing: {
    container_max_width: string;
    container_padding: string;
    section_margin: string;
    item_margin: string;
  };
  borders: {
    header: string;
    section: string;
  };
}

export interface FieldStyles {
  [key: string]: {
    prefix_md?: string;
    suffix_md?: string;
    separator?: string;
    bullet_md?: string;
    bullet_txt?: string;
  };
}

export interface ResumeConfig {
  field_styles: FieldStyles;
  theme: Theme;
}

export function loadConfig(): ResumeConfig {
  const configPath = path.join(process.cwd(), "resume", "00-config.md");
  const fileContent = fs.readFileSync(configPath, "utf-8");
  const { data } = matter(fileContent);
  return data as ResumeConfig;
}

export function themeToCSS(theme: Theme): string {
  return `
    :root {
      --color-primary: ${theme.colors.primary};
      --color-text: ${theme.colors.text};
      --color-text-secondary: ${theme.colors.text_secondary};
      --color-bg: ${theme.colors.background};
      --color-border: ${theme.colors.border};

      --font-family: ${theme.fonts.family};
      --font-size-base: ${theme.fonts.size_base};
      --font-size-h1: ${theme.fonts.size_h1};
      --font-size-h2: ${theme.fonts.size_h2};
      --font-size-h3: ${theme.fonts.size_h3};
      --font-size-small: ${theme.fonts.size_small};

      --max-width: ${theme.spacing.container_max_width};
      --container-padding: ${theme.spacing.container_padding};
      --section-margin: ${theme.spacing.section_margin};
      --item-margin: ${theme.spacing.item_margin};

      --border-header: ${theme.borders.header};
      --border-section: ${theme.borders.section};
    }
  `;
}
