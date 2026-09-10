import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(scriptDirectory, "..");
const faviconTag = '  <link rel="icon" type="image/svg+xml" href="/favicon.svg">';

async function htmlFiles(directory, relative = "") {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    if ([".git", "node_modules", "assets"].includes(entry.name)) continue;
    const absolute = path.join(directory, entry.name);
    const rel = path.join(relative, entry.name);
    if (entry.isDirectory()) files.push(...await htmlFiles(absolute, rel));
    else if (entry.isFile() && entry.name.endsWith(".html") && !entry.name.startsWith("google")) files.push(rel);
  }

  return files;
}

let changed = 0;
for (const relativePath of await htmlFiles(root)) {
  const absolutePath = path.join(root, relativePath);
  let html = await readFile(absolutePath, "utf8");
  if (/rel=["'](?:shortcut\s+)?icon["']/i.test(html)) continue;

  if (/<meta name=["']theme-color["'][^>]*>/i.test(html)) {
    html = html.replace(/(<meta name=["']theme-color["'][^>]*>)/i, `$1\n${faviconTag}`);
  } else if (/<head>/i.test(html)) {
    html = html.replace(/<head>/i, `<head>\n${faviconTag}`);
  } else {
    continue;
  }

  await writeFile(absolutePath, html, "utf8");
  changed += 1;
}

console.log(`Favicon verificado en el sitio. Archivos modificados: ${changed}.`);
