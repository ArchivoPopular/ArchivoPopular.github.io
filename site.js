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
