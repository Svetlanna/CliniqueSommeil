import os
import re
import sqlite3

from etl.extract import recuperer_donnees
from etl.transform import calculer_indicateurs
from etl.load import sauvegarder_resultats


def get_ids_nuit_disponibles():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dossier = os.path.join(base_dir, "raw", "traite")
    ids = []
    for nom in sorted(os.listdir(dossier)):
        match = re.search(r"nuit-(\d+)\.csv$", nom)
        if match:
            ids.append(int(match.group(1)))
    return ids


def get_ids_nuit_deja_traites():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "datalake.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='curated_nuit'")
    if not cursor.fetchone():
        conn.close()
        return set()
    cursor.execute("SELECT DISTINCT id_nuit FROM curated_nuit")
    ids = {row[0] for row in cursor.fetchall()}
    conn.close()
    return ids


def run_pipeline(id_nuit):
    queries_response: dict = recuperer_donnees(id_nuit)
    df_capteur = queries_response['df_capteur']
    print(f"Étape 1 : Extraction :\n    {len(df_capteur)} lignes lues dans le CSV.\n    {queries_response['nbr_events'][0]} événements dans la base MySQL.")

    print("Étape 2 : Calcul des indicateurs...")
    indicateurs = calculer_indicateurs(
        queries_response['df_capteur'],
        queries_response['df_events'],
        queries_response['nbapnees'],
        queries_response['nbhypopnees'],
        queries_response['nbrera'],
        queries_response['nbr_events']
    )

    print("Étape 3 : Sauvegarde dans le Datalake...")
    sauvegarder_resultats(indicateurs, id_nuit)


ids_disponibles = get_ids_nuit_disponibles()
ids_traites = get_ids_nuit_deja_traites()

print(f"Nuits disponibles : {ids_disponibles}")
print(f"Nuits déjà dans le datalake : {sorted(ids_traites)}\n")

for id_nuit in ids_disponibles:
    if id_nuit in ids_traites:
        print(f"--- Nuit {id_nuit} : déjà présente dans le datalake, ignorée.")
        continue
    print(f"--- Pipeline nuit {id_nuit} ---")
    run_pipeline(id_nuit)
    print()

print("Pipeline terminé.")
