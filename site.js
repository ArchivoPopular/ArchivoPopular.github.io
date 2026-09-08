const menuButton = document.querySelector(".menu-button");
const siteNav = document.querySelector(".site-nav");
const brandbar = document.querySelector(".brandbar");
const siteScript = [...document.scripts].find((script) => /(?:^|\/)site\.js(?:\?|$)/.test(script.src));
const siteRoot = new URL(".", siteScript?.src || window.location.href);

window.archivoPopularRoot = siteRoot.href;

if (brandbar && menuButton) {
  const headerActions = document.createElement("div");
  const searchLink = document.createElement("a");

  headerActions.className = "header-actions";
  searchLink.className = "header-search-link";
  searchLink.href = new URL("buscar.html", siteRoot).href;
  searchLink.setAttribute("aria-label", "Buscar en Archivo Popular");
  searchLink.innerHTML = `
    <svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22">
      <circle cx="11" cy="11" r="6.75"></circle>
      <path d="m16 16 4.25 4.25"></path>
    </svg>
    <span>Buscar</span>`;

  if (window.location.pathname.endsWith("/buscar.html")) {
    searchLink.setAttribute("aria-current", "page");
  }

  headerActions.append(searchLink, menuButton);
  brandbar.append(headerActions);
}

if (menuButton && siteNav) {
  menuButton.addEventListener("click", () => {
    const isOpen = siteNav.dataset.open === "true";
    siteNav.dataset.open = String(!isOpen);
    menuButton.setAttribute("aria-expanded", String(!isOpen));
  });

  siteNav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      siteNav.dataset.open = "false";
      menuButton.setAttribute("aria-expanded", "false");
    });
  });
}

document.querySelectorAll("[data-current-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});

// Publicaciones del 8 de setiembre de 2026.
// Se inyectan sobre las grillas estáticas para mantener portada y Noticias actualizadas.
const fmedStory = {
  url: new URL("noticias/udelar-movilizacion-medicina-violencia-genero-2026.html", siteRoot).href,
  image: new URL("assets/news/fmed-movilizacion-santiago-ares-2026.webp", siteRoot).href,
  title: "La Udelar se moviliza frente a Medicina: “La violencia de género es estructural”",
  summary: "La Intergremial de la Udelar convocó una movilización frente a Medicina y Química, una semana después del intento de femicidio contra una estudiante. La AEM levantó la ocupación, pero mantiene nuevas medidas.",
  category: "Universidad pública · Violencia de género",
  date: "8 SEP 2026",
  place: "Montevideo · Uruguay",
  credit: "Foto: Santiago Ares / Archivo Popular"
};

const pisaStory = {
  url: new URL("noticias/pisa-2025-uruguay-ciencias-matematica-lectura-2026.html", siteRoot).href,
  image: "https://imagenes.montevideo.com.uy/imgnoticias/202609/_W933_80/970436.jpg",
  title: "PISA 2025: Uruguay lidera la región en ciencias y matemática, pero cae en lectura",
  summary: "Uruguay obtuvo 445 puntos en ciencias, 405 en matemática y 423 en lectura. ANEP señaló la lectura como la alerta más urgente y la OCDE volvió a mostrar brechas socioeconómicas persistentes.",
  category: "Educación pública · Desigualdad y aprendizajes",
  date: "8 SEP 2026",
  place: "Montevideo · Uruguay",
  credit: "Foto: ANEP"
};

const makeStoryCard = (story, storyId, alt) => {
  const link = document.createElement("a");
  link.className = "news-card";
  link.href = story.url;
  link.dataset.storyId = storyId;
  link.innerHTML = `<figure><img src="${story.image}" alt="${alt}" loading="lazy"></figure><div class="news-card__body"><p class="eyebrow">${story.category}</p><h2>${story.title}</h2><p>${story.summary}</p><p class="story-meta"><span>${story.date}</span><span>${story.place}</span></p></div>`;
  return link;
};

const latestStory = document.querySelector("[data-latest-story]");
if (latestStory && !window.location.pathname.includes("/noticias/")) {
  latestStory.innerHTML = `<figure><img src="${fmedStory.image}" alt="Movilización de la comunidad universitaria frente a la Facultad de Medicina en Montevideo"><figcaption class="photo-credit">${fmedStory.credit} · 8 de setiembre de 2026</figcaption></figure><div class="lead-copy"><p class="story-meta"><span>${fmedStory.date}</span><span>${fmedStory.place}</span></p><h1 id="ultima-noticia">${fmedStory.title}</h1><p class="summary">${fmedStory.summary}</p><a class="story-link" href="${fmedStory.url}">Leer la noticia completa</a></div>`;

  const homeGrid = document.querySelector("[data-home-news-grid]");
  if (homeGrid) {
    if (!homeGrid.querySelector('a[href*="paro-nacional-universidades-argentina-financiamiento-2026.html"]')) {
      const previousPrevious = document.createElement("a");
      previousPrevious.className = "news-card";
      previousPrevious.href = new URL("noticias/paro-nacional-universidades-argentina-financiamiento-2026.html", siteRoot).href;
      previousPrevious.innerHTML = `<figure><img src="${new URL("assets/news/paro-universitario-argentina-uba-mayo-2026.jpg", siteRoot).href}" alt="Movilización en defensa de la universidad pública durante la Marcha Federal Universitaria de mayo de 2026 en Buenos Aires" width="658" height="425" loading="lazy"></figure><div class="news-card__body"><p class="eyebrow">América Latina · Universidad pública y trabajo</p><h2>Universidades argentinas paran en todo el país por salarios y financiamiento y preparan una quinta Marcha Federal</h2><p>Docentes y nodocentes realizan un paro nacional de 24 horas por salarios, financiamiento y cumplimiento de la Ley 27.795.</p><p class="story-meta"><span>8 SEP 2026</span><span>Argentina</span></p></div>`;
      homeGrid.prepend(previousPrevious);
    }
    if (!homeGrid.querySelector('[data-story-id="pisa-2025-uruguay"]') && !homeGrid.querySelector('a[href*="pisa-2025-uruguay-ciencias-matematica-lectura-2026.html"]')) {
      homeGrid.prepend(makeStoryCard(pisaStory, "pisa-2025-uruguay", "Presentación oficial de los resultados PISA Uruguay 2025 realizada por la ANEP en Montevideo"));
    }
  }
}

const newsGrid = document.querySelector("[data-news-grid]");
if (newsGrid) {
  if (!newsGrid.querySelector('[data-story-id="pisa-2025-uruguay"]') && !newsGrid.querySelector('a[href*="pisa-2025-uruguay-ciencias-matematica-lectura-2026.html"]')) {
    newsGrid.prepend(makeStoryCard(pisaStory, "pisa-2025-uruguay", "Presentación oficial de los resultados PISA Uruguay 2025 realizada por la ANEP en Montevideo"));
  }
  if (!newsGrid.querySelector('[data-story-id="fmed-movilizacion-2026"]') && !newsGrid.querySelector('a[href*="udelar-movilizacion-medicina-violencia-genero-2026.html"]')) {
    newsGrid.prepend(makeStoryCard(fmedStory, "fmed-movilizacion-2026", "Movilización de la comunidad universitaria frente a la Facultad de Medicina en Montevideo"));
  }
}
