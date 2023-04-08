# Copyright 2022 Lilya Benladjreb BENL28549807
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask import render_template
from flask import g
from flask import request
from database import Database
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import csv
import sqlite3

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


# Fonction pour extraire les données de la ville de Montréal et les mettre à jour dans la base de données
def update_database():
    url = 'https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv'
    response = requests.get(url)
    data = response.content.decode('utf-8')
    csv_reader = csv.DictReader(data.splitlines())
    contrevenants = [dict(row) for row in csv_reader]
    conn = sqlite3.connect('db/db.db')
    cursor = conn.cursor()
    for contrevenant in contrevenants:
        # Vérifier si la ligne existe déjà dans la base de données avant de l'insérer
        cursor.execute('SELECT * FROM contrevenants WHERE id_poursuite = ?', (contrevenant[0],))
        existing_row = cursor.fetchone()
        if existing_row is None:
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
    conn.commit()
    conn.close()


# Configuration du BackgroundScheduler pour exécuter la fonction update_database() chaque jour à minuit
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_database, trigger="cron", hour=0, minute=0)
scheduler.start()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route("/")
def index():
    return render_template("index.html")


# Sert à renvoyer la page 404 lorsque source introuvable
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# Sert pour le moteur de recherche
@app.route("/recherche")
def recherche():
    database = Database()
    query = request.args.get('query').lower()
    contrevenants = database.get_all_contrevenants()
    filter_contrevenants = _filter_contrevenants(contrevenants, query)
    return render_template('resultat.html', contrevenants=filter_contrevenants)


# Sert à filtrer les contrevenants par nom d'établissement, propriétaire et rue
def _filter_contrevenants(contrevenants, query):
    filter_contrevenants = []
    for contrevenant in contrevenants:
        term = (contrevenant['etablissement'] + contrevenant['adresse'] + contrevenant['proprietaire']).lower()
        if query in term:
            filter_contrevenants.append(contrevenant)
    return filter_contrevenants
