const API_BASE_URL = "http://localhost:5000";

// Fonction pour afficher uniquement la section sélectionnée
function showSection(sectionId) {
  // Masquer toutes les sections
  document.querySelectorAll('main > div').forEach((section) => {
    section.classList.add('d-none');
  });

  // Afficher la section sélectionnée
  const targetSection = document.getElementById(sectionId);
  if (targetSection) {
    targetSection.classList.remove('d-none');
  } else {
    console.error(`Section with ID "${sectionId}" not found.`);
  }

  // Gérer l'état actif dans le menu
  document.querySelectorAll('.navbar.fixed-bottom .nav-link').forEach((link) => {
    link.classList.remove('active');
  });

  const activeLink = document.querySelector(`[onclick="showSection('${sectionId}')"]`);
  if (activeLink) {
    activeLink.classList.add('active');
  } else {
    console.error(`Link for section "${sectionId}" not found.`);
  }
}

// Charger les membres
function loadMembres() {
  fetch(`${API_BASE_URL}/membres`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Failed to fetch membres: ${response.statusText}`);
      }
      return response.json();
    })
    .then((membres) => {
      const membresList = document.getElementById("membres-list");
      if (membresList) {
        if (membres.length === 0) {
          membresList.innerHTML = `<p class="text-muted text-center">Aucun membre trouvé.</p>`;
        } else {
          membresList.innerHTML = membres.map((membre) => `
            <div class="col-md-4">
              <div class="card shadow">
                <div class="card-body">
                  <h5 class="card-title">${membre.nom}</h5>
                  <p class="card-text">${membre.profession}</p>
                  <p class="text-muted">Âge : ${membre.age}</p>
                </div>
              </div>
            </div>
          `).join("");
        }
      }
    })
    .catch((err) => console.error("Erreur lors du chargement des membres :", err));
}

// Charger les entités
function loadEntites() {
  fetch(`${API_BASE_URL}/entites`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Failed to fetch entites: ${response.statusText}`);
      }
      return response.json();
    })
    .then((entites) => {
      const entitesList = document.getElementById("entites-list");
      if (entitesList) {
        if (entites.length === 0) {
          entitesList.innerHTML = `<p class="text-muted text-center">Aucune entité trouvée.</p>`;
        } else {
          entitesList.innerHTML = entites.map((entite) => `
            <li class="list-group-item">${entite.nom}</li>
          `).join("");
        }
      }
    })
    .catch((err) => console.error("Erreur lors du chargement des entités :", err));
}

// Charger les cartes
function loadCartes() {
  fetch(`${API_BASE_URL}/cartes`)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Failed to fetch cartes: ${response.statusText}`);
      }
      return response.json();
    })
    .then((cartes) => {
      const cartesList = document.getElementById("cartes-list");
      if (cartesList) {
        if (cartes.length === 0) {
          cartesList.innerHTML = `<tr><td colspan="4" class="text-center text-muted">Aucune carte trouvée.</td></tr>`;
        } else {
          cartesList.innerHTML = cartes.map((carte) => `
            <tr>
              <td>${carte.id}</td>
              <td>${carte.membre_id}</td>
              <td>${carte.statut}</td>
              <td>${new Date(carte.date_delivrance).toLocaleDateString()}</td>
            </tr>
          `).join("");
        }
      }
    })
    .catch((err) => console.error("Erreur lors du chargement des cartes :", err));
}

// Charger les données au chargement
document.addEventListener("DOMContentLoaded", () => {
  try {
    showSection('welcome-section'); // Par défaut, afficher la section d'accueil
    loadMembres();
    loadEntites();
    loadCartes();
  } catch (err) {
    console.error("Erreur lors de l'initialisation :", err);
  }

  // Initialisation de la modale
  const addMembreButton = document.querySelector('[data-bs-toggle="modal"]');
  const modalElement = document.getElementById('addMembreModal');

  if (addMembreButton && modalElement) {
    const modalInstance = new bootstrap.Modal(modalElement);

    addMembreButton.addEventListener('click', () => {
      modalElement.classList.remove('d-none');
      modalInstance.show();
    });

    modalElement.addEventListener('hidden.bs.modal', () => {
      modalElement.classList.add('d-none');
    });
  }
});

// Ajouter un membre
const addMembreForm = document.getElementById("addMembreForm");
if (addMembreForm) {
  addMembreForm.addEventListener("submit", async function (e) {
    e.preventDefault(); // Empêcher le rechargement de la page

    const form = e.target;
    const formData = Object.fromEntries(new FormData(form)); // Convertir les données du formulaire en objet

    try {
      const response = await fetch(`${API_BASE_URL}/membres`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        loadMembres(); // Recharger la liste des membres
        form.reset(); // Réinitialiser le formulaire

        // Fermer le modal correctement
        const modalElement = document.getElementById("addMembreModal");
        const modalInstance = bootstrap.Modal.getInstance(modalElement);
        if (modalInstance) {
          modalInstance.hide();
        }
      } else {
        console.error("Erreur lors de l'ajout du membre :", response.statusText);
      }
    } catch (err) {
      console.error("Erreur lors de l'ajout du membre :", err);
    }
  });
} else {
  console.error("Formulaire 'addMembreForm' introuvable.");
}
