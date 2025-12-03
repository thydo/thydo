/**
 * Resume content utilities
 */
import { getCollection } from "astro:content";

export type ResumeEntry = Awaited<ReturnType<typeof getCollection<"resume">>>[number];

/**
 * Get resume entries for a section, excluding header files (00-)
 */
export async function getResumeItems(sectionPrefix: string): Promise<ResumeEntry[]> {
  const allEntries = await getCollection("resume");
  return allEntries
    .filter(e => e.id.startsWith(`${sectionPrefix}/`) && !e.id.includes("/00-"))
    .sort((a, b) => a.id.localeCompare(b.id));
}

/**
 * Extract item name from entry id (e.g., "04-experience/01-company.md" -> "company")
 */
export function getItemName(entry: ResumeEntry): string {
  return entry.id.split('/').pop()?.replace(/^\d+-/, '').replace('.md', '') || '';
}

/**
 * Render markdown-like content to HTML with subsections
 * Handles **bold**, bullet lists, and **Header:** subsection patterns
 */
export function renderContent(content: string): string {
  if (!content) return "";

  let html = content.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  const cleanItem = (item: string) => item.replace(/^-\s*/, "").trim();
  const sections = html.split(/(?=<strong>[^<]+:<\/strong>)/);

  return sections.map(section => {
    const headerMatch = section.match(/^<strong>([^<]+):<\/strong>/);
    if (headerMatch) {
      const header = headerMatch[1];
      const rest = section.replace(/^<strong>[^<]+:<\/strong>\s*/, "");
      const items = rest.split(/\n-\s*/).filter(Boolean);
      const listHtml = items.map(item => `<li>${cleanItem(item)}</li>`).join("\n");
      return `<div class="subsection"><h4>${header}</h4><ul>${listHtml}</ul></div>`;
    }
    const items = section.split(/\n-\s*/).filter(Boolean);
    if (items.length > 0) {
      const listHtml = items.map(item => `<li>${cleanItem(item)}</li>`).join("\n");
      return `<ul>${listHtml}</ul>`;
    }
    return section;
  }).join("\n");
}
