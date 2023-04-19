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

    # Permet de créer un nouvel utilisateur dns la bd
    def create_user(self, nom_user, prenom_user, email, salt, hash):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(("insert into users (nom_user, prenom_user,"
                        " adresse_courriel, salt, hash) values(?, ?,"
                        " ?, ?, ?)"),
                       (nom_user, prenom_user, email, salt, hash))
        conn.commit()
        return cursor.lastrowid

    # Permet de dresser une liste d'établissements par utilisateur
    # (user peut donc créer plusieurs listes à son nom"
    def create_request(self, user_id, etablissements):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(("insert into follow_requests (id_user, etablissements)"
                        " values (?, ?)"), (user_id, etablissements))
        conn.commit()

    # Permet de dresser une liste d'établissements qui indique leur nom
    # et nombre de contraventions recues
    def get_list_contrevenants(self):
        cursor = self.get_connection().cursor()
        query = ("select etablissement, count(id_poursuite) as nb_infractions "
                 "from contrevenants group by etablissement "
                 "order by nb_infractions desc ")
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    # Permet de dresser une liste des mises à jour
    def get_list_new_contrevenants(self, new_id):
        cursor = self.get_connection().cursor()
        query = "select * from contrevenants where id = ?"
        cursor.execute(query, (new_id,))
        return [dict(row) for row in cursor.fetchall()]

    # Permet de créer une nouvelle demande d'inspection
    def post_inspection(self, etablissement, adresse, ville, date_visite,
                        nom_user, prenom_user, problem):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(("insert into inspection_requests "
                        "(etablissement, adresse, ville, date_visite,"
                        " nom_user, prenom_user, description_problem) "
                        "values (?, ?, ?, ?, ?, ?, ?)"),
                       (etablissement, adresse, ville, date_visite, nom_user,
                        prenom_user, problem))
        conn.commit()

    # Permet de supprimer une demande d'inspection
    def delete_inspection(self, etablissement, nom_user, prenom_user, ville):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(("delete from inspection_requests where nom_user = ? "
                        "AND prenom_user = ? "
                        "AND etablissement = ? AND ville = ?"),
                       (nom_user, prenom_user, etablissement, ville))
        conn.commit()
