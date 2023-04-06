# Auteur: Lilya Benladjreb
# Code Permanent: BENL28549807
#
# Description : Classe servant à l'utilisation de la database

import sqlite3
from datetime import date

# Créer un objet contrevenant
def _build_contrevenant(result_set_item):
    contrevenant = {}
    contrevenant["id"] = result_set_item[0]
    contrevenant["id_poursuite"] = result_set_item[1]
    contrevenant["business_id"] = result_set_item[2]
    contrevenant["etablissement"] = result_set_item[3]
    contrevenant["categorie"] = result_set_item[4]
    contrevenant["adresse"] = result_set_item[5]
    contrevenant["description"] = result_set_item[6]
    contrevenant["proprietaire"] = result_set_item[7]
    contrevenant["date_infraction"] = result_set_item[8]
    contrevenant["date_jugement"] = result_set_item[9]
    contrevenant["montant"] = result_set_item[10]
    return contrevenant


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
    def get_all_contrevenants(self):
        cursor = self.get_connection().cursor()
        query = ("select * from contrevenants")
        cursor.execute(query)
        all_data = cursor.fetchall()
        return [_build_contrevenant(item) for item in all_data]
    