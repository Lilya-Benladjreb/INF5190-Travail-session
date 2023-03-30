# Auteur: Lilya Benladjreb
# Code Permanent: BENL28549807
#
# Description: Classe permet l'implémentation de script dans le projet
#
import csv
import sqlite3
import requests

# URL des données à télécharger
url = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

# Téléchargement des données
response = requests.get(url)

# Extraction des données CSV
csv_data = response.content.decode('utf-8')

# Connexion à la base de données SQLite
conn = sqlite3.connect('db/db.db')

# Création d'un objet curseur
cursor = conn.cursor()

reader = csv.reader(csv_data.splitlines())

# Boucle pour parcourir chaque ligne du fichier CSV et insérer les données dans la base de données
for row in reader:
    # Sauter la première ligne (en-têtes de colonne)
    next(reader)

    # Extraction des colonnes souhaitées
    cols_selected = (row[0], row[1], row[6], row[12], row[4], row[3], row[7], row[2], row[5], row[7])
    id_poursuite = row[0]
    business_id = row[1]
    etablissement = row[6]
    categorie = row[12]
    adresse = row[4]
    description = row[3]
    proprietaire = row[7]
    date_infraction = row[2]
    date_jugement = row[5]
    montant = row[7]

    cursor.execute("INSERT INTO contrevenants (id_poursuite, business_id, etablissement, categorie, adresse, description, proprietaire, date_infraction, date_jugement, montant) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", cols_selected)

# Valider la transaction
conn.commit()

# Fermer la connexion à la base de données
conn.close()



