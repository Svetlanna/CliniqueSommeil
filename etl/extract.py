import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def recuperer_donnees(id_nuit : int):
    # lecture du CSV
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin_csv = os.path.join(base_dir, "raw", "traite", f"signal-psg-patient-{id_nuit}-nuit-{id_nuit}.csv")
    df_capteur = pd.read_csv(chemin_csv)

    # lecture des événements (MySQL)
    conn = mysql.connector.connect(
        host=os.environ.get("host"),
        user=os.environ.get("user"),
        password=os.environ.get("password"),
        database=os.environ.get("database")
    )
    cur = conn.cursor()
    query = f'SELECT * FROM evenement_respiratoire WHERE id_nuit = {id_nuit}'
    cur.execute(query)
    df_events = cur.fetchall()
    conn.close()

    return df_capteur, df_events