const searchForm = document.querySelector("[data-search-form]");
const searchInput = document.querySelector("[data-search-input]");
const searchStatus = document.querySelector("[data-search-status]");
const searchResults = document.querySelector("[data-search-results]");
const searchSuggestions = document.querySelectorAll("[data-search-suggestion]");
const searchScript = [...document.scripts].find((script) => /(?:^|\/)buscador\.js(?:\?|$)/.test(script.src));
const searchRoot = new URL(".", searchScript?.src || window.location.href);
const titleCollator = new Intl.Collator("es", { sensitivity: "base" });

let searchEntries = [];
let searchReady = false;
let inputTimer;

function normalizeText(value = "") {
  return String(value)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9ñÑ]+/g, " ")
    .trim()
    .toLowerCase();
}

function compactText(value = "") {
  return String(value).replace(/\s+/g, " ").trim();
}

function shortText(value, limit = 250) {
  const text = compactText(value);
  if (text.length <= limit) return text;
  return `${text.slice(0, limit).replace(/\s+\S*$/, "")}…`;
}

function searchableEntry(entry) {
  const keywords = Array.isArray(entry.keywords) ? entry.keywords.join(" ") : (entry.keywords || "");
  const fields = {
    title: normalizeText(entry.title),
    summary: normalizeText(entry.summary),
    body: normalizeText(entry.body),
    keywords: normalizeText(keywords),
    category: normalizeText(entry.category),
    date: normalizeText(entry.dateDisplay || entry.date),
    place: normalizeText(entry.place)
  };

  return {
    ...entry,
    url: new URL(entry.url, searchRoot).href,
    _fields: fields,
    _all: Object.values(fields).join(" ")
  };
}

function entryScore(entry, query) {
  const normalizedQuery = normalizeText(query);
  const terms = [...new Set(normalizedQuery.split(" ").filter(Boolean))];
  if (!terms.length || !terms.every((term) => entry._all.includes(term))) return null;

  const fields = entry._fields;
  let score = 0;

  if (fields.title === normalizedQuery) score += 500;
  else if (fields.title.includes(normalizedQuery)) score += 220;
  if (fields.keywords.includes(normalizedQuery)) score += 130;
  if (fields.summary.includes(normalizedQuery)) score += 80;
  if (fields.body.includes(normalizedQuery)) score += 25;
  if (fields.category.includes(normalizedQuery)) score += 60;
  if (fields.place.includes(normalizedQuery)) score += 45;
  if (fields.date.includes(normalizedQuery)) score += 45;

  terms.forEach((term) => {
    if (fields.title.includes(term)) score += 45;
    if (fields.keywords.includes(term)) score += 24;
    if (fields.summary.includes(term)) score += 14;
    if (fields.category.includes(term)) score += 12;
    if (fields.place.includes(term) || fields.date.includes(term)) score += 8;
    if (fields.body.includes(term)) score += 3;
  });

  return score;
}

function resultCard(entry) {
  const link = document.createElement("a");
  const top = document.createElement("div");
  const type = document.createElement("span");
  const category = document.createElement("span");
  const title = document.createElement("h2");
  const summary = document.createElement("p");
  const meta = document.createElement("p");

  link.className = "search-result";
  link.href = entry.url;
  top.className = "search-result__top";
  type.className = "search-result__type";
  category.className = "search-result__category";
  title.className = "search-result__title";
  summary.className = "search-result__summary";
  meta.className = "search-result__meta";

  type.textContent = entry.type || "Artículo";
  category.textContent = entry.category || "";
  title.textContent = entry.title;
  summary.textContent = shortText(entry.summary || entry.body);
  meta.textContent = [entry.dateDisplay || entry.date, entry.place].filter(Boolean).join(" · ");

  top.append(type);
  if (category.textContent) top.append(category);
  link.append(top, title);
  if (summary.textContent) link.append(summary);
  if (meta.textContent) link.append(meta);

  return link;
}

function renderSearch(query) {
  const cleanQuery = compactText(query);
  searchResults.replaceChildren();

  if (cleanQuery.length < 2) {
    searchStatus.textContent = "Escribí al menos dos caracteres para comenzar.";
    return;
  }

  if (!searchReady) {
    searchStatus.textContent = "Preparando el archivo…";
    return;
  }

  const matches = searchEntries
    .map((entry) => ({ entry, score: entryScore(entry, cleanQuery) }))
    .filter((result) => result.score !== null)
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      const dateDifference = new Date(b.entry.date || 0) - new Date(a.entry.date || 0);
      if (dateDifference) return dateDifference;
      return titleCollator.compare(a.entry.title, b.entry.title);
    });

  const visibleMatches = matches.slice(0, 30);
  const count = matches.length;
  searchStatus.textContent = count === 1
    ? `1 resultado para “${cleanQuery}”`
    : `${count} resultados para “${cleanQuery}”`;

  if (!count) {
    const empty = document.createElement("div");
    const heading = document.createElement("h2");
    const text = document.createElement("p");
    empty.className = "search-empty";
    heading.textContent = "No encontramos coincidencias";
    text.textContent = "Probá con menos palabras, otro nombre o un término más general.";
    empty.append(heading, text);
    searchResults.append(empty);
    return;
  }

  visibleMatches.forEach(({ entry }) => searchResults.append(resultCard(entry)));

  if (count > visibleMatches.length) {
    const remainder = document.createElement("p");
    remainder.className = "search-remainder";
    remainder.textContent = `Se muestran los primeros ${visibleMatches.length} resultados. Agregá otra palabra para precisar la búsqueda.`;
    searchResults.append(remainder);
  }
}

function updateQuery(query, replace = true) {
  const url = new URL(window.location.href);
  const cleanQuery = compactText(query);
  if (cleanQuery) url.searchParams.set("q", cleanQuery);
  else url.searchParams.delete("q");
  window.history[replace ? "replaceState" : "pushState"]({}, "", url);
}

function fallbackNewsEntry(story) {
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
    keywords: [story.id, story.category, story.place]
  };
}

async function loadSearchIndex() {
  searchStatus.textContent = "Preparando el archivo…";

  const [indexResult, newsResult] = await Promise.allSettled([
    fetch(new URL("data/buscador.json", searchRoot), { cache: "no-store" }).then((response) => {
      if (!response.ok) throw new Error(`Índice: HTTP ${response.status}`);
      return response.json();
    }),
    fetch(new URL("data/noticias.json", searchRoot), { cache: "no-store" }).then((response) => {
      if (!response.ok) throw new Error(`Noticias: HTTP ${response.status}`);
      return response.json();
    })
  ]);

  const indexedItems = indexResult.status === "fulfilled"
    ? (Array.isArray(indexResult.value) ? indexResult.value : indexResult.value.items || [])
    : [];
  const newsItems = newsResult.status === "fulfilled" && Array.isArray(newsResult.value)
    ? newsResult.value
    : [];
  const merged = new Map(indexedItems.map((item) => [item.url, item]));

  newsItems.forEach((story) => {
    if (!merged.has(story.url)) merged.set(story.url, fallbackNewsEntry(story));
  });

  searchEntries = [...merged.values()].map(searchableEntry);
  searchReady = searchEntries.length > 0;

  if (!searchReady) {
    searchStatus.textContent = "El buscador no pudo cargar el archivo. Intentá nuevamente en unos minutos.";
    return;
  }

  renderSearch(searchInput.value);
}

if (searchForm && searchInput && searchStatus && searchResults) {
  const initialQuery = new URL(window.location.href).searchParams.get("q") || "";
  searchInput.value = initialQuery;

  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    clearTimeout(inputTimer);
    updateQuery(searchInput.value);
    renderSearch(searchInput.value);
  });

  searchInput.addEventListener("input", () => {
    clearTimeout(inputTimer);
    inputTimer = window.setTimeout(() => renderSearch(searchInput.value), 120);
  });

  searchSuggestions.forEach((button) => {
    button.addEventListener("click", () => {
      const suggestion = button.dataset.searchSuggestion || "";
      searchInput.value = suggestion;
      updateQuery(suggestion);
      renderSearch(suggestion);
      searchInput.focus();
    });
  });

  window.addEventListener("popstate", () => {
    const query = new URL(window.location.href).searchParams.get("q") || "";
    searchInput.value = query;
    renderSearch(query);
  });

  loadSearchIndex().catch((error) => {
    console.warn("No se pudo cargar el buscador.", error);
    searchStatus.textContent = "El buscador no pudo cargar el archivo. Intentá nuevamente en unos minutos.";
  });
}
