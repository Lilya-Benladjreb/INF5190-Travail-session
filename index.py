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

app = Flask(__name__, static_url_path="", static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


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
    query = request.args.get('query').lower()
    contrevenants = get_db().get_all_contrevenants()
    return render_template('resultat.html', contrevenants=filter_contrevenants)


# Sert à filtrer les contrevenants par nom d'établissement, propriétaire et rue
def _filter_contrevenants(contrevenants, query):
    filter_contrevenants = []
    for contrevenant in contrevenants:
        if query in contrevenants['etablissement'].lower():
            filter_contrevenants.append(contrevenant)
        elif query in contrevenant['proprietaire'].lower():
            filter_contrevenants.append(contrevenant)
        elif query in contrevenant['adresse'].lower():
            filter_contrevenants.append(contrevenant)
    return filter_contrevenants