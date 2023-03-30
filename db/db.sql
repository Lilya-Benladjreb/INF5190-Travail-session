CREATE TABLE contrevenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_poursuite INTEGER,
    business_id INTEGER,
    etablissement TEXT,
    categorie TEXT,
    adresse TEXT,
    description TEXT,
    proprietaire TEXT,
    date_infraction TEXT,
    date_jugement TEXT,
    montant REAL
);


