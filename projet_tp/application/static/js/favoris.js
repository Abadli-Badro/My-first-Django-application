let initialFavoris = [
  { name: "Facture", path: "/achat/facture/ajouter" },
  { name: "Clients", path: "/clients/ajouter/" },
  { name: "Bon", path: "/achat/bon_commande" },
  { name: "Achat", path: "/achat/" },
  { name: "Vente", path: "/vente/" },
  { name: "Stock", path: "/stock/" },
  { name: "Fournire", path: "/fournisseurs/" },
  { name: "Produits", path: "/produits/" },
];

let favoris = [
  { name: "Vente", path: "/vente/" },
  { name: "Produits", path: "/produits/" },
];

const favorisUl = document.querySelector(".features-box");
const addButton = document.querySelector("#addButton");
const deleteButton = document.querySelector("#deleteButton");
const selectHtml = document.querySelector("select#cars");

selectHtml.innerHTML = initialFavoris
  .map(({ name, path }) => `<option value="${path}">${name}</option>;`)
  .join("\n");

addButton.addEventListener("click", () => {
  const { selectedIndex } = selectHtml;
  if (!favoris.includes(initialFavoris[selectedIndex])) {
    favoris.push(initialFavoris[selectedIndex]);
  }
  displayFavoris();
});

deleteButton.addEventListener("click", () => {
  const { selectedIndex } = selectHtml;
  favoris = favoris.filter(
    ({ path }) => path !== initialFavoris[selectedIndex].path
  );
  displayFavoris();
});

const displayFavoris = () => {
  favorisUl.innerHTML = favoris
    .map(
      ({ name, path }) => `<a href="${path}" class="feature col-4">${name}</a>`
    )
    .join("\n");
};

displayFavoris();
