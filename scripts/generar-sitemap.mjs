import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(scriptDirectory, "..");
const siteUrl = (process.env.SITE_URL || "https://archivopopular.github.io").replace(/\/+$/, "");

const corePages = [
  ["index.html", "/"],
  ["noticias.html", "/noticias.html"],
  ["historia.html", "/historia.html"],
  ["personajes.html", "/personajes.html"],
  ["fotografos.html", "/fotografos.html"],
  ["bio_santiagoares.html", "/bio_santiagoares.html"]
];

function escapeXml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&apos;");
}

function attribute(tag, name) {
  return tag.match(new RegExp(`\\b${name}\\s*=\\s*["']([^"']+)["']`, "i"))?.[1] || "";
}

function isNoIndex(html) {
  for (const match of html.matchAll(/<meta\b[^>]*>/gi)) {
    const tag = match[0];
    if (attribute(tag, "name").toLowerCase() !== "robots") continue;
    if (attribute(tag, "content").toLowerCase().split(/[,\s]+/).includes("noindex")) return true;
  }
  return false;
}

function extractLastmod(html) {
  const jsonLdDate = html.match(/"dateModified"\s*:\s*"([^"]+)"/i)?.[1];
  if (jsonLdDate) return jsonLdDate.slice(0, 10);

  for (const match of html.matchAll(/<meta\b[^>]*>/gi)) {
    const tag = match[0];
    if (attribute(tag, "property").toLowerCase() !== "article:published_time") continue;
    const published = attribute(tag, "content");
    if (published) return published.slice(0, 10);
  }

  return "";
}

async function pageEntry(relativePath, publicPath, includeLastmod = false) {
  const html = await readFile(path.join(root, relativePath), "utf8");
  if (isNoIndex(html)) return null;

  return {
    loc: `${siteUrl}${publicPath}`,
    lastmod: includeLastmod ? extractLastmod(html) : ""
  };
}

const entries = [];

for (const [relativePath, publicPath] of corePages) {
  entries.push(await pageEntry(relativePath, publicPath));
}

const newsDirectory = path.join(root, "noticias");
const newsFiles = (await readdir(newsDirectory))
  .filter((file) => file.endsWith(".html"))
  .sort((a, b) => a.localeCompare(b, "es"));

for (const file of newsFiles) {
  const entry = await pageEntry(
    path.join("noticias", file),
    `/noticias/${encodeURI(file)}`,
    true
  );
  if (entry) entries.push(entry);
}

const uniqueEntries = [...new Map(entries.filter(Boolean).map((entry) => [entry.loc, entry])).values()];

if (uniqueEntries.length !== entries.filter(Boolean).length) {
  throw new Error("El sitemap contenía URLs duplicadas.");
}

const xml = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...uniqueEntries.map(({ loc, lastmod }) =>
    lastmod
      ? `  <url><loc>${escapeXml(loc)}</loc><lastmod>${escapeXml(lastmod)}</lastmod></url>`
      : `  <url><loc>${escapeXml(loc)}</loc></url>`
  ),
  '</urlset>',
  ''
].join("\n");

await writeFile(path.join(root, "sitemap.xml"), xml, "utf8");
console.log(`Sitemap creado: ${uniqueEntries.length} URLs (${newsFiles.length} noticias).`);
