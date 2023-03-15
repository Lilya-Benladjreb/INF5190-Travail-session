create table violations (
    id integer primary key, 
    id_poursuite integer,
    business_id integer,
    date_infraction text,
    description_infraction varchar(500),
    adresse varchar(100),
    etablissement varchar(100),
    proprietaire varchar(100),
    montant_infraction integer
);

