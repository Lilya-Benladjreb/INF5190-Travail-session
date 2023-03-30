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
conn = sqlite3.connect('db.db')

# Création d'un objet curseur
cursor = conn.cursor()

# Boucle pour parcourir chaque ligne du fichier CSV et insérer les données dans la base de données
for row in csv.reader(csv_data.splitlines()):
    cursor.execute("INSERT INTO contrevenants (nom, categorie, description, date_infraction, date_jugement, montant) VALUES (?, ?, ?, ?, ?, ?)", row)

# Valider la transaction
conn.commit()

# Fermer la connexion à la base de données
conn.close()



