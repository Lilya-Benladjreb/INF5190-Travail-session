# Auteur: Lilya Benladjreb
# Code Permanent: BENL28549807
#
# Description: Classe permet l'implémentation de script dans le projet
#
import csv
import sqlite3
import requests
from datetime import datetime

# URL des données à télécharger
url = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

# Téléchargement des données
response = requests.get(url)

# Extraction des données CSV
csv_data = response.content.decode('utf-8')

# Convertir les données CSV en liste de dictionnaires
csv_reader = csv.DictReader(csv_data.splitlines())
contrevenants = [dict(row) for row in csv_reader]

for contrevenant in contrevenants:
    date_obj = datetime.strptime(contrevenant['date'], '%Y%m%d')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    contrevenant['date'] = formatted_date
    date_jugement_obj = datetime.strptime(contrevenant['date_jugement'], '%Y%m%d')
    formatted_date_jugement = date_jugement_obj.strftime('%Y-%m-%d')
    contrevenant['date_jugement'] = formatted_date_jugement

# Connexion à la base de données SQLite
conn = sqlite3.connect('db/db.db')
cursor = conn.cursor()

# Boucle pour parcourir chaque ligne du fichier CSV et insérer les données dans la base de données
for contrevenant in contrevenants:
    cursor.execute("""
        INSERT INTO contrevenants (
            id_poursuite,
            business_id,
            etablissement,
            categorie,
            adresse,
            description,
            proprietaire,
            date_infraction,
            date_jugement,
            montant
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        contrevenant['id_poursuite'],
        contrevenant['business_id'],
        contrevenant['etablissement'],
        contrevenant['categorie'],
        contrevenant['adresse'],
        contrevenant['description'],
        contrevenant['proprietaire'],
        contrevenant['date'],
        contrevenant['date_jugement'],
        contrevenant['montant']
    ))
# Valider la transaction et fermer la connection
conn.commit()
conn.close()


