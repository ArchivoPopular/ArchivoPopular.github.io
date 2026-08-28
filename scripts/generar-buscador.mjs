import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(scriptDirectory, "..");

async function read(relativePath) {
  return readFile(path.join(root, relativePath), "utf8");
}

function decodeEntities(value = "") {
  const named = {
    amp: "&",
    apos: "'",
    gt: ">",
    hellip: "…",
    laquo: "«",
    ldquo: "“",
    lsquo: "‘",
    lt: "<",
    mdash: "—",
    nbsp: " ",
    ndash: "–",
    quot: '"',
    raquo: "»",
    rdquo: "”",
    rsquo: "’"
  };

  return value
    .replace(/&#x([0-9a-f]+);/gi, (_, number) => String.fromCodePoint(Number.parseInt(number, 16)))
    .replace(/&#(\d+);/g, (_, number) => String.fromCodePoint(Number.parseInt(number, 10)))
    .replace(/&([a-z]+);/gi, (entity, name) => named[name.toLowerCase()] ?? entity);
}

function textFromHtml(value = "") {
  return decodeEntities(
    value
      .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
      .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ")
      .replace(/<svg\b[^>]*>[\s\S]*?<\/svg>/gi, " ")
      .replace(/<br\s*\/?>/gi, " ")
      .replace(/<\/p>|<\/h[1-6]>|<\/li>|<\/div>/gi, " ")
      .replace(/<[^>]+>/g, " ")
  ).replace(/\s+/g, " ").trim();
}

function firstTag(block, tag) {
  const match = block.match(new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, "i"));
  return textFromHtml(match?.[1] || "");
}

function firstClass(block, className) {
  const match = block.match(new RegExp(`<[^>]+class=["'][^"']*\\b${className}\\b[^"']*["'][^>]*>([\\s\\S]*?)<\\/[^>]+>`, "i"));
  return textFromHtml(match?.[1] || "");
}

function paragraphTexts(block, excludedClass = "") {
  return [...block.matchAll(/<p\b([^>]*)>([\s\S]*?)<\/p>/gi)]
    .filter((match) => !excludedClass || !match[1].includes(excludedClass))
    .map((match) => textFromHtml(match[2]))
    .filter(Boolean);
}

function articleBlock(html) {
  return html.match(/<article\b[^>]*class=["'][^"']*\barticle-shell\b[^"']*["'][^>]*>([\s\S]*?)<\/article>/i)?.[1]
    || html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)?.[1]
    || html;
}

async function newsEntries() {
  const stories = JSON.parse(await read("data/noticias.json"));

  return Promise.all(stories.map(async (story) => {
    let body = story.summary;
    try {
      body = textFromHtml(articleBlock(await read(story.url)));
    } catch {
      console.warn(`No se encontró ${story.url}; se indexan título y resumen.`);
    }

    return {
      id: story.id,
      type: story.archive ? "Archivo" : "Noticia",
      title: story.title,
      summary: story.summary,
      category: story.category,
      date: story.date,
      dateDisplay: story.dateDisplay,
      place: story.place,
      url: story.url,
      keywords: [story.id, story.category, story.place, story.archive ? "archivo histórico" : "actualidad"],
      body
    };
  }));
}

async function historyEntries() {
  const html = await read("historia.html");
  const matches = [...html.matchAll(/<article\b[^>]*class=["'][^"']*\bhistory-entry\b[^"']*["'][^>]*id=["']([^"']+)["'][^>]*>([\s\S]*?)<\/article>/gi)];

  return matches.map(([, id, block]) => {
    const paragraphs = paragraphTexts(block, "history-entry__date");
    return {
      id,
      type: "Historia",
      title: firstTag(block, "h3"),
      summary: paragraphs[0] || "",
      category: "Historia de las izquierdas",
      dateDisplay: firstClass(block, "history-entry__date"),
      place: "",
      url: `historia.html#${id}`,
      keywords: [id, "historia", "izquierda", "memoria", "revolución", "movimiento obrero"],
      body: textFromHtml(block)
    };
  });
}

async function politicalEntries() {
  const html = await read("personajes.html");
  const matches = [...html.matchAll(/<article\b[^>]*class=["'][^"']*\bperson-card\b[^"']*["'][^>]*id=["']([^"']+)["'][^>]*>([\s\S]*?)<\/article>/gi)];

  return matches.map(([, id, block]) => {
    const paragraphs = paragraphTexts(block, "eyebrow");
    const category = firstClass(block, "eyebrow");
    return {
      id,
      type: "Archivo político",
      title: firstTag(block, "h2"),
      summary: paragraphs[0] || "",
      category,
      dateDisplay: "",
      place: category,
      url: `personajes.html#${id}`,
      keywords: [id, "personaje histórico", "ideas", "izquierda", category],
      body: textFromHtml(block)
    };
  });
}

async function photographerEntries() {
  const html = await read("bio_santiagoares.html");
  const main = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)?.[1] || html;
  const summary = "Fotógrafo, fotoperiodista y creador audiovisual uruguayo dedicado a documentar política, memoria, movilizaciones y vida social.";

  return [{
    id: "santiago-ares",
    type: "Fotografía",
    title: "Santiago Ares",
    summary,
    category: "Fotógrafos de Archivo Popular",
    dateDisplay: "Montevideo · Desde 2022",
    place: "Montevideo · Uruguay",
    url: "bio_santiagoares.html",
    keywords: ["Santiago Ares", "fotógrafo", "fotoperiodista", "fotografía", "Archivo Popular", "ph.ares"],
    body: textFromHtml(main)
  }];
}

async function institutionalEntries() {
  const html = await read("index.html");
  const section = html.match(/<section\b[^>]*id=["']nosotros["'][^>]*>([\s\S]*?)<\/section>/i)?.[1] || "";

  return [{
    id: "archivo-popular",
    type: "Institucional",
    title: "Archivo Popular: nuestra mirada",
    summary: "Un medio de noticias, memoria y fotografía con una mirada popular, progresista y latinoamericana.",
    category: "Sobre Archivo Popular",
    dateDisplay: "Desde 2023",
    place: "Montevideo · Uruguay",
    url: "index.html#nosotros",
    keywords: ["Archivo Popular", "medio", "nosotros", "línea editorial", "progresismo", "izquierda"],
    body: textFromHtml(section)
  }];
}

const groups = {
  news: await newsEntries(),
  history: await historyEntries(),
  political: await politicalEntries(),
  photographers: await photographerEntries(),
  institutional: await institutionalEntries()
};

if (groups.history.length !== 10) {
  throw new Error(`Se esperaban 10 procesos históricos y se encontraron ${groups.history.length}.`);
}

if (groups.political.length !== 19) {
  throw new Error(`Se esperaban 19 protagonistas y se encontraron ${groups.political.length}.`);
}

const items = Object.values(groups).flat();
const duplicateUrls = items
  .map((item) => item.url)
  .filter((url, index, urls) => urls.indexOf(url) !== index);

if (duplicateUrls.length) {
  throw new Error(`Hay direcciones duplicadas en el índice: ${[...new Set(duplicateUrls)].join(", ")}`);
}

await writeFile(
  path.join(root, "data", "buscador.json"),
  `${JSON.stringify({ version: 1, items }, null, 2)}\n`,
  "utf8"
);

console.log(
  `Índice creado: ${items.length} entradas (${groups.news.length} noticias, ${groups.history.length} historias, ${groups.political.length} protagonistas, ${groups.photographers.length} fotógrafos y ${groups.institutional.length} institucional).`
);
