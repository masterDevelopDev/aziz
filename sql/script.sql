DROP DATABASE IF EXISTS solidarite;
CREATE DATABASE solidarite;
USE solidarite;

-- Table Solidarité
CREATE TABLE solidarite (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Utilisez INT pour clé primaire
    nom VARCHAR(255) NOT NULL
);

-- Table Entités de Solidarité
CREATE TABLE entites_solidarite (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Même type que la clé primaire
    nom VARCHAR(255) NOT NULL, -- Exemple: "المكتب التنفيذي"
    solidarite_id INT REFERENCES solidarite(id) ON DELETE CASCADE -- Type compatible
);

-- Table des Rôles dans la Solidarité
CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Utilisez INT pour clé primaire
    nom VARCHAR(255) NOT NULL -- Exemple: "Président", "Secrétaire"
);

-- Table des Membres des Entités
CREATE TABLE membres_entites (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Utilisez INT pour clé primaire
    nom VARCHAR(255) NOT NULL,
    profession VARCHAR(255), -- Profession dans la vie courante
    age INT,
    genre VARCHAR(20), -- Homme, Femme
    telephone VARCHAR(20),
    lieu_travail VARCHAR(255),
    niveau_academique VARCHAR(255),
    carte_adhesion VARCHAR(20) UNIQUE NOT NULL, -- Numéro de carte d'adhésion
    entite_id INT REFERENCES entites_solidarite(id) ON DELETE CASCADE,
    role_id INT REFERENCES roles(id) ON DELETE SET NULL -- Type compatible
);

-- Table des Cartes d'Adhésion
CREATE TABLE cartes_adhesion (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Utilisez INT pour clé primaire
    membre_id INT REFERENCES membres_entites(id) ON DELETE CASCADE,
    date_delivrance DATE NOT NULL,
    statut VARCHAR(50) NOT NULL, -- Délivrée, Payée, Non payée, En suspens
    montant DECIMAL(10, 2),
    date_statut DATE NOT NULL
);

-- Table de l'Historique des Participations
CREATE TABLE historique_participations (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Utilisez INT pour clé primaire
    membre_id INT REFERENCES membres_entites(id) ON DELETE CASCADE,
    entite_id INT REFERENCES entites_solidarite(id) ON DELETE CASCADE,
    role_id INT REFERENCES roles(id) ON DELETE SET NULL, -- Type compatible
    date_debut DATE NOT NULL,
    date_fin DATE,
    commentaire TEXT
);

INSERT INTO solidarite (nom) VALUES
('Solidarité nationale');

INSERT INTO entites_solidarite (nom, solidarite_id) VALUES
('المكتب التنفيذي', 1),
('المجلس الإداري', 1),
('الجمع العام', 1),
('لجنة المراقبة', 1),
('الثلث الخارج', 1);

INSERT INTO roles (nom) VALUES
('Président'),
('Secrétaire'),
('Trésorier'),
('Membre');

INSERT INTO membres_entites (nom, profession, age, genre, telephone, lieu_travail, niveau_academique, carte_adhesion, entite_id, role_id) VALUES
('Ahmed El Mansouri', 'Enseignant', 45, 'Homme', '0612345678', 'Rabat', 'Bac+5', 'A001', 1, 1),
('Fatima Zohra', 'Comptable', 40, 'Femme', '0623456789', 'Casablanca', 'Bac+4', 'A002', 2, 2),
('Youssef Amrani', 'Ingénieur', 38, 'Homme', '0654321987', 'Tanger', 'Bac+5', 'A003', 3, 3),
('Nadia Lahlou', 'Avocate', 35, 'Femme', '0678912345', 'Marrakech', 'Bac+6', 'A004', 4, 4);

INSERT INTO cartes_adhesion (membre_id, date_delivrance, statut, montant, date_statut) VALUES
(1, '2024-01-01', 'Délivrée', 100.00, '2024-01-01'),
(2, '2023-01-01', 'Payée', 150.00, '2023-03-01'),
(3, '2023-06-01', 'Non payée', 100.00, '2023-07-01'),
(4, '2022-01-01', 'En suspens', 0.00, '2022-12-01');

INSERT INTO historique_participations (membre_id, entite_id, role_id, date_debut, date_fin, commentaire) VALUES
(1, 1, 1, '2021-01-01', NULL, 'Président actif'),
(2, 2, 2, '2020-01-01', '2022-12-31', 'A terminé son mandat'),
(3, 3, 3, '2022-01-01', NULL, 'Actif en tant que trésorier'),
(4, 4, 4, '2021-01-01', '2023-01-01', 'Participation terminée');