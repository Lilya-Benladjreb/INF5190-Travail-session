CREATE TABLE contrevenants (
    id INTEGER PRIMARY KEY ,
    id_poursuite INTEGER,
    business_id INTEGER,
    etablissement varchar(100),
    categorie varchar(50),
    adresse varchar(100),
    description varchar(255),
    proprietaire varchar(100),
    date_infraction varchar(10),
    date_jugement varchar(10),
    montant DECIMAL(8,2)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    nom_user varchar(50),
    prenom_user varchar(50),
    adresse_courriel varchar(100),
    id_request varchar(255) REFERENCES follow_requests(id_request),
    salt varchar(32),
    hash varchar(128)
);

CREATE TABLE follow_requests(
    id_request INTEGER PRIMARY KEY,
    id_user INTEGER REFERENCES users(id),
    etablissements varchar(255)
);

CREATE TABLE inspection_requests(
    id_inspection INTEGER PRIMARY KEY,
    etablissement varchar(100) REFERENCES contrevenants(etablissement),
    adresse varchar(100),
    ville varchar(50),
    date_visite varchar(10),
    nom_user varchar(50),
    prenom_user varchar(50),
    description_problem varchar(255)
);
