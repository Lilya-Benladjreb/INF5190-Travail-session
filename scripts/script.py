# Auteur: Lilya Benladjreb
# Code Permanent: BENL28549807
#
# Description: Classe permet l'implémentation de script dans le projet
#

import pandas as pd
import sqlite3

# Lire le fichier CSV et le transformer en DataFrame
df = pd.read_csv('https://donnees.montreal.ca/dataset/9f6c0b6b-7b1e-4f40-aa28-63642bf9b53e/resource/fcdfdc5b-b5d9-4e7b-9f5e-33f869bb2d31/download/inspection-aliments-contrevenants.csv')

# Create a SQLite database and connect to it
conn = sqlite3.connect('db.db')

# Use the to_sql() method of the DataFrame to insert the data into a new table in the database
df.to_sql('violations', conn)

# Close the database connection
conn.close()

