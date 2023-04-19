# Auteur: Lilya Benladjreb
# Code Permanent: BENL28549807
#
# Description: Classe permet l'implémentation des schemas dans le projet
#

formulaire_profil_utilisateur = {
    "type": "object",
    "properties": {
        "nom_user": {"type": "string"},
        "prenom_user": {"type": "string"},
        "adresse_courriel": {"type": "string"},
        "etablissements": {"type": "array", "items": {"type": "string"}},
        "mot_de_passe": {"type": "string"}
    },
    "required": ["nom_user", "prenom_user", "adresse_courriel", "etablissements", "mot_de_passe"],
    "additionalProperties": False
}

formulaire_demande_inspection = {
    "type": "object",
    "properties": {
        "etablissement": {"type": "string"},
        "adresse": {"type": "string"},
        "ville": {"type": "string"},
        "date_visite": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
        "nom_user": {"type": "string"},
        "prenom_user": {"type": "string"},
        "description_problem": {"type": "string"}
    },
    "required": ["etablissement", "adresse", "ville", "date_visite", "nom_user", "prenom_user",
                 "description_problem"],
    "additionalProperties": False
}

formulaire_supprimer_inspection = {
    "type": "object",
    "properties": {
        "etablissement": {"type": "string"},
        "ville": {"type": "string"},
        "nom_user": {"type": "string"},
        "prenom_user": {"type": "string"},
    },
    "required": ["etablissement", "ville", "nom_user", "prenom_user"],
    "additionalProperties": False
}
