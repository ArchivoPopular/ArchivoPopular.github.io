function storyMeta(story) {
  return `<p class="story-meta"><span>${story.dateDisplay}</span><span>${story.place}</span></p>`;
}

function latestStory(story) {
  return `
    <figure>
      <img src="${story.image}" alt="${story.imageAlt}" width="750" height="500">
      <figcaption class="photo-credit">Foto: ${story.photoCredit}</figcaption>
    </figure>
    <div class="lead-copy">
      ${storyMeta(story)}
      <h1 id="ultima-noticia">${story.title}</h1>
      <p class="summary">${story.summary}</p>
      <a class="story-link" href="${story.url}">Leer la noticia</a>
    </div>`;
}

function newsCard(story) {
  return `
    <a class="news-card" href="${story.url}">
      <figure><img src="${story.image}" alt="${story.imageAlt}" width="750" height="500" loading="lazy"></figure>
      <div class="news-card__body">
        <p class="eyebrow">${story.category}</p>
        <h2>${story.title}</h2>
        <p>${story.summary}</p>
        ${storyMeta(story)}
      </div>
    </a>`;
}

async function loadNews() {
  const latestContainer = document.querySelector("[data-latest-story]");
  const gridContainer = document.querySelector("[data-news-grid]");
  const homeGridContainer = document.querySelector("[data-home-news-grid]");
  if (!latestContainer && !gridContainer && !homeGridContainer) return;

  try {
    const response = await fetch("data/noticias.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const stories = await response.json();
    if (!Array.isArray(stories) || stories.length === 0) return;

    stories.sort((a, b) => new Date(b.date) - new Date(a.date));
    if (latestContainer) latestContainer.innerHTML = latestStory(stories[0]);
    if (gridContainer) gridContainer.innerHTML = stories.map(newsCard).join("");
    if (homeGridContainer) {
      const previousStories = stories.slice(1, 7);
      homeGridContainer.innerHTML = previousStories.length
        ? previousStories.map(newsCard).join("")
        : '<p class="news-empty">Las próximas publicaciones aparecerán acá.</p>';
    }
  } catch (error) {
    console.warn("No se pudo actualizar el archivo de noticias; se conserva el contenido estático.", error);
  }
}

loadNews();
