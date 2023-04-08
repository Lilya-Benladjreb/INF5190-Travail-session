# Auteur: Lilya Benladjreb
# Code Permanent: BENL28549807
#
# Description : Classe servant à l'utilisation de la database

import sqlite3


# Créer un objet contrevenant

class Database:
    def __init__(self):
        self.connection = None

    # Établit la connection
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/db.db')
            self.connection.row_factory = sqlite3.Row
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
        return [dict(row) for row in cursor.fetchall()]
