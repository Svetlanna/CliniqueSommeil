import sqlite3

def sauvegarder_resultats(indicateurs, id_nuit):
    # Connexion au Datalake
    conn = sqlite3.connect('datalake.db')
    cursor = conn.cursor()
