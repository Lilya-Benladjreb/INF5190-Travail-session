create table violations (
    id integer primary key, 
    id_poursuite integer,
    id_business integer,
    infraction_date text,
    infraction_description varchar(500),
    adresse varchar(100),
    jugement_date text,
    etablissement varchar(100),
    infraction_montant integer,
    proprietaire varchar(100),
    ville varchar(50),
    statut varchar(100),
    statut_date text,
    categorie varchar(100)
);

