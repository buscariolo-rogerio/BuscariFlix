const searchForm = document.querySelector("#search-form");
const searchInput = document.querySelector("#movie-search");
const clearButton = document.querySelector("#clear-search");
const cards = [...document.querySelectorAll(".movie-card")];
const groups = [...document.querySelectorAll("[data-group]")];
const status = document.querySelector("#search-status");
const emptyState = document.querySelector("#empty-state");

const normalize = (value) => value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase("pt-BR").trim();

function filterCatalog() {
  const query = normalize(searchInput.value);
  let visibleCount = 0;
  cards.forEach((card) => {
    const matches = normalize(`${card.dataset.title} ${card.dataset.year}`).includes(query);
    card.hidden = !matches;
    if (matches) visibleCount += 1;
  });
  groups.forEach((group) => { group.hidden = !group.querySelector(".movie-card:not([hidden])"); });
  clearButton.hidden = query.length === 0;
  emptyState.hidden = visibleCount !== 0;
  status.textContent = query ? `${visibleCount} ${visibleCount === 1 ? "resultado" : "resultados"} para “${searchInput.value.trim()}”` : `${cards.length} títulos disponíveis`;
}

searchForm.addEventListener("submit", (event) => event.preventDefault());
searchInput.addEventListener("input", filterCatalog);
clearButton.addEventListener("click", () => { searchInput.value = ""; filterCatalog(); searchInput.focus(); });
