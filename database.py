# Auteur: Lilya Benladjreb
# Code Permanent: BENL28549807
#
# Description : Classe servant à l'utilisation de la database

import sqlite3
from datetime import date

# Créer un objet infraction
def _build_infraction(result_set_item):
    infraction = {}
    infraction["id"] = result_set_item[0]
    infraction["id_poursuite"] = result_set_item[1]
    infraction["id_business"] = result_set_item[2]
    infraction["infraction_date"] = result_set_item[3]
    infraction["infraction_description"] = result_set_item[4]
    infraction["adresse"] = result_set_item[5]
    infraction["jugement_date"] = result_set_item[4]
    infraction["infraction_montant"] = result_set_item[8]
    infraction["etablissement"] = result_set_item[6]
    infraction["infraction_montant"] = result_set_item[8]
    infraction["proprietaire"] = result_set_item[7]
    infraction["ville"] = result_set_item[7]
    infraction["statut"] = result_set_item[7]
    infraction["statut_date"] = result_set_item[7]
    infraction["categorie"] = result_set_item[7]


class Database:
    def __init__(self):
        self.connection = None

    # Établit la connection
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/db.db')
        return self.connection

    # Déconnection de la base de donnée
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    # Créer une liste de toutes les infractions se trouvant dans la bd
    def get_all_infractions(self):
        cursor = self.get_connection().cursor()
        query = ("select * form violations order by infraction_date desc, id desc")
        cursor.execute(query)
        infractions = cursor.fetchall()
        return
