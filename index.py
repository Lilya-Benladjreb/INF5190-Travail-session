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
import json

from flask import Flask, render_template, g, request, jsonify
from database import Database
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import csv
import sqlite3

app = Flask(__name__, static_url_path="", static_folder="static")
app.config['JSON_AS_ASCII'] = False

INFRACTION_URL = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1" \
                 "-b208-d8744dca8fc6/download/violations.csv "


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


# Fonction pour extraire les données de la ville de Montréal et les mettre à jour dans la base de données
def update_database():
    url = INFRACTION_URL
    response = requests.get(url)
    data = response.content.decode('utf-8')
    csv_reader = csv.DictReader(data.splitlines())
    contrevenants = [dict(row) for row in csv_reader]
    conn = sqlite3.connect('db/db.db')
    cursor = conn.cursor()
    for contrevenant in contrevenants:
        # Vérifier si la ligne existe déjà dans la base de données avant de l'insérer
        cursor.execute("SELECT * FROM contrevenants WHERE id_poursuite = ?", (contrevenant[0],))
        existing_row = cursor.fetchone()
        if existing_row is None:
            cursor.execute("\n"
                           "                INSERT INTO contrevenants (\n"
                           "                    id_poursuite,\n"
                           "                    business_id,\n"
                           "                    etablissement,\n"
                           "                    categorie,\n"
                           "                    adresse,\n"
                           "                    description,\n"
                           "                    proprietaire,\n"
                           "                    date_infraction,\n"
                           "                    date_jugement,\n"
                           "                    montant\n"
                           "                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)\n"
                           "            ", (
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


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Sert à renvoyer la page 404 lorsque source introuvable
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


# Sert pour le moteur de recherche par établissement
@app.route("/recherche-etablissement", methods=["GET"])
def recherche_etablissement():
    database = Database()
    query = request.args.get('etablissement').lower()
    contrevenants = database.get_all_contrevenants()
    filter_contrevenants = _filter_contrevenants_etablissement(contrevenants, query)
    return render_template('resultat.html', contrevenants=filter_contrevenants)


# Sert pour le moteur de recherche par propriétaire
@app.route("/recherche-proprietaire", methods=["GET"])
def recherche_proprietaire():
    database = Database()
    query = request.args.get('proprietaire').lower()
    contrevenants = database.get_all_contrevenants()
    filter_contrevenants = _filter_contrevenants_proprietaire(contrevenants, query)
    return render_template('resultat.html', contrevenants=filter_contrevenants)


# Sert pour le moteur de recherche par adresse
@app.route("/recherche-adresse", methods=["GET"])
def recherche_adresse():
    database = Database()
    query = request.args.get('adresse').lower()
    contrevenants = database.get_all_contrevenants()
    filter_contrevenants = _filter_contrevenants_adresse(contrevenants, query)
    return render_template('resultat.html', contrevenants=filter_contrevenants)


# Route qui affiche la documentation des services REST de l'application
@app.route("/doc/", methods=['GET'])
def get_doc():
    return render_template("doc.html")


# Sert au service REST permettant d'obtenir la liste des contrevenants ayant commis une infraction entre deux dates
@app.route("/api/contrevenants", methods=['GET'])
def get_contrevenant():
    database = Database()
    contrevenants = database.get_all_contrevenants()
    start_date = request.args.get('du')
    end_date = request.args.get('au')

    if not start_date:
        response = {'message': "Paramètre 'du' manquant."}
        return app.response_class(json.dumps(response, ensure_ascii=False), status=400,
                                  mimetype='application/json; charset=utf-8')
    if not end_date:
        response = {'message': "Paramètre 'au' manquant."}
        return app.response_class(json.dumps(response, ensure_ascii=False), status=400,
                                  mimetype='application/json; charset=utf-8')

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        response = {'error': 'Format de date invalide. Utilisez le format ISO 8601 (AAAA-MM-JJ).'}
        return app.response_class(json.dumps(response, ensure_ascii=False), status=400,
                                  mimetype='application/json; charset=utf-8')

    filter_contrevenants = [c for c in contrevenants if
                            start_date <= datetime.strptime(c['date_infraction'], '%Y-%m-%d') <= end_date]

    return jsonify(filter_contrevenants), 200


# Sert à la requête Ajax permettant de saisir deux dates. Affiche la liste des contrevenants dans un tableau.
@app.route("/recherche-date", methods=["GET"])
def recherche_date():
    query_du = request.args.get("date-du")
    query_au = request.args.get("date-au")
    database = Database()
    contrevenants = database.get_all_contrevenants()

    if not query_du:
        response = {'message': "Paramètre 'du' manquant."}
        return app.response_class(json.dumps(response, ensure_ascii=False), status=400,
                                  mimetype='application/json; charset=utf-8')
    if not query_au:
        response = {'message': "Paramètre 'au' manquant."}
        return app.response_class(json.dumps(response, ensure_ascii=False), status=400,
                                  mimetype='application/json; charset=utf-8')

    filter_contrevenants = _filter_contrevenants_date(contrevenants, query_du, query_au)

    response = jsonify(filter_contrevenants)
    response.headers.add('Content-Type', 'application/json; charset=utf-8')

    return response, 200


# Sert à filtrer les contraventions par nom d'établissement
def _filter_contrevenants_etablissement(contrevenants, query):
    filter_contrevenants = []
    for contrevenant in contrevenants:
        term = contrevenant['etablissement'].lower()
        if query in term:
            filter_contrevenants.append(contrevenant)
    return filter_contrevenants


# Sert à filtrer les contraventions par propriétaire
def _filter_contrevenants_proprietaire(contrevenants, query):
    filter_contrevenants = []
    for contrevenant in contrevenants:
        term = contrevenant['proprietaire'].lower()
        if query in term:
            filter_contrevenants.append(contrevenant)
    return filter_contrevenants


# Sert à filtrer les contraventions par adresse
def _filter_contrevenants_adresse(contrevenants, query):
    filter_contrevenants = []
    for contrevenant in contrevenants:
        term = contrevenant['adresse'].lower()
        if query in term:
            filter_contrevenants.append(contrevenant)
    return filter_contrevenants


# Sert à filter les contraventions par date
def _filter_contrevenants_date(contrevenants, query_du, query_au):
    filter_contrevenants = []
    for contrevenant in contrevenants:
        term = contrevenant['date_infraction']
        if query_au >= term >= query_du:
            filter_contrevenants.append(contrevenant)
    return filter_contrevenants
