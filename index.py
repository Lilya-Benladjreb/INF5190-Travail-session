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
import hashlib
import smtplib
import ssl
import uuid
import requests
import csv
import sqlite3
import yaml
from flask import Flask, render_template, g, request, jsonify, Response
from database import Database
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from schemas.schema import formulaire_profil_utilisateur, formulaire_demande_inspection
from jsonschema import validate, ValidationError
from io import StringIO

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
    rows = csv.reader(data.splitlines())
    next(rows)
    with sqlite3.connect('db/db.db') as conn:
        liste_nouveaux_contrevenants = []
        contrevenants = [dict(row) for row in rows]
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
                liste_nouveaux_contrevenants.append(cursor.lastrowid())
        conn.commit()
        conn.close()
    return liste_nouveaux_contrevenants


# Sert à lister les changements lorsqu'il y a des mises à jour au fichier csv de la ville
def creer_liste_nouveaux_changements():
    liste_des_nouveaux_id = update_database()

    for new_id in liste_des_nouveaux_id:
        new_data = get_db().get_list_new_contrevenants(new_id).append()

    result = new_data
    return result


# Sert à créer l'email contenant les mises à jour de la BD
def envoyer_liste_de_changements():
    liste_new_data = creer_liste_nouveaux_changements()
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        receiver_email = config["email"]

    if liste_new_data:
        sender_email = "lilyatest28@gmail.com"  # Replacer par sender email
        password = "Neo283417!!"  # Replace par actual sender email password
        subject = "Derniers ajouts aux données ouvertes - Violations.csv"
        body = "\n".join([", ".join(row) for row in liste_new_data])
        message = f"Subject: {subject}\n\n{body}"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)


# Configuration du BackgroundScheduler pour exécuter la fonction update_database() chaque jour à minuit
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_database, trigger="cron", hour=0, minute=0)
scheduler.start()


# Ce qui doit être arrêté lorsque l'application Flask s'arrête
@app.teardown_appcontext
def close_connection(exception):
    # Déconnection à la BD
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


# Route de base
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
    query = request.args.get('etablissement').lower()
    contrevenants = get_db().get_all_contrevenants()
    filter_contrevenants = _filter_contrevenants_etablissement(contrevenants, query)
    return render_template('resultat.html', contrevenants=filter_contrevenants)


# Sert pour le moteur de recherche par propriétaire
@app.route("/recherche-proprietaire", methods=["GET"])
def recherche_proprietaire():
    query = request.args.get('proprietaire').lower()
    contrevenants = get_db().get_all_contrevenants()
    filter_contrevenants = _filter_contrevenants_proprietaire(contrevenants, query)
    return render_template('resultat.html', contrevenants=filter_contrevenants)


# Sert pour le moteur de recherche par adresse
@app.route("/recherche-adresse", methods=["GET"])
def recherche_adresse():
    query = request.args.get('adresse').lower()
    contrevenants = get_db().get_all_contrevenants()
    filter_contrevenants = _filter_contrevenants_adresse(contrevenants, query)
    return render_template('resultat.html', contrevenants=filter_contrevenants)


# Route qui affiche la documentation des services REST de l'application
@app.route("/doc/", methods=['GET'])
def get_doc():
    return render_template("doc.html")


# Sert au service REST permettant d'obtenir la liste des contrevenants ayant commis une infraction entre deux dates
@app.route("/api/contrevenants", methods=['GET'])
def get_contrevenant():
    contrevenants = get_db().get_all_contrevenants()
    start_date = request.args.get('du')
    end_date = request.args.get('au')

    if not start_date:
        response = {'error': "Paramètre 'du' manquant."}
        return jsonify(response), 400
    if not end_date:
        response = {'error': "Paramètre 'au' manquant."}
        return jsonify(response), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        response = {'error': 'Format de date invalide. Utilisez le format ISO 8601 (AAAA-MM-JJ).'}
        return jsonify(response), 400

    filter_contrevenants = [c for c in contrevenants if
                            start_date <= datetime.strptime(c['date_infraction'], '%Y-%m-%d') <= end_date]

    return jsonify(filter_contrevenants), 200


# Sert à créer un nouvel utilisateur dans la BD
@app.route('/api/post-user', methods=['POST'])
def create_user():
    json_data = request.get_json()

    try:
        validate(instance=json_data, schema=formulaire_profil_utilisateur)
    except Exception as e:
        return {"status": "error", "message": "Validation failed", "errors": str(e)}, 422

    nom_user = json_data['nom_user']
    prenom_user = json_data['prenom_user']
    email = json_data['adresse_courriel']
    etablissements = ','.join(json_data['etablissements'])
    password = json_data['mot_de_passe']

    if nom_user == "" or prenom_user == "" or password == "" or email == "" or etablissements == "":
        return jsonify({'error': 'svp remplir tous les champs demandés'}), 400
    else:
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
        user_id = get_db().create_user(nom_user, prenom_user, email, salt, hashed_password)
        get_db().create_request(user_id, etablissements)
    return jsonify({'message': 'Profil utilisateur créé avec succès'}), 201


# Sert à recevoir la liste de tous les établissements ainsi que leur nombre d'infractions en ordre décroissant (json)
@app.route('/api/get-etablissements-by-infractions-json', methods=['GET'])
def get_etablissements_by_infractions_json():
    ordered_contrevenants = get_db().get_list_contrevenants()
    response = jsonify(ordered_contrevenants)

    return response, 200


# Sert à recevoir la liste de tous les établissements ainsi que leur nombre d'infractions en ordre décroissant (XML)
@app.route('/api/get-etablissements-by-infractions-xml', methods=['GET'])
def get_etablissements_xml():
    try:
        contrevenants = get_db().get_list_contrevenants()
        return render_template('etablissement-par-contraventions.xml', contrevenants=contrevenants), 200

    except Exception as e:
        return jsonify(
            {'error': 'Erreur lors de la connexion à la base de données', 'details': str(e)}), 500


# Sert à recevoir la liste de tous les établissements ainsi que leur nombre d'infractions en ordre décroissant (CSV)
@app.route('/api/get-etablissements-by-infractions-csv', methods=['GET'])
def get_etablissements_by_infractions_csv():
    ordered_contrevenants = get_db().get_list_contrevenants()

    csv_data = StringIO()
    fieldnames = ['etablissement', 'nb_infractions']
    writer = csv.DictWriter(csv_data, fieldnames=fieldnames)

    # Écrire CSV data dans le StringIO object
    writer.writeheader()
    for contrevenant in ordered_contrevenants:
        writer.writerow(contrevenant)

    # Retourner le CSV data en réponse Flask
    response = Response(csv_data.getvalue(), mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename='contrevenants.csv')
    return response, 200


# Sert à offrir un service REST permettant de faire une demande d'inspection à la ville.
@app.route("/api/post-inspection", methods=["POST"])
def create_inspection_request():
    json_data = request.get_json()
    try:
        validate(instance=json_data, schema=formulaire_demande_inspection)
    except Exception as e:
        return {"status": "error", "message": "Validation échouée", "errors": str(e)}, 422

    etablissement = json_data['etablissement']
    nom_user = json_data['nom_user']
    prenom_user = json_data['prenom_user']
    adresse = json_data['adresse']
    ville = json_data['ville']
    date_visite = json_data['date_visite']
    probleme = json_data['description_problem']

    if etablissement == "" or nom_user == "" or prenom_user == "" or adresse == "" \
            or ville == "" or date_visite == "" or probleme == "":
        return jsonify({'error': 'svp remplir tous les champs demandés'}), 400
    else:
        get_db().post_inspection(etablissement, adresse, ville, date_visite, nom_user, prenom_user, probleme)
        return jsonify({"message": "Demande d'inspection effectuée avec succès"}), 201


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
