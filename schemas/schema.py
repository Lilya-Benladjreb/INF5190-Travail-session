# Auteur: Lilya Benladjreb
# Code Permanent: BENL28549807
#
# Description: Classe permet l'implémentation des schemas dans le projet
#

from .common import ma
from marshmallow import fields, validate

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
