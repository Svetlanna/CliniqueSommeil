import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def recuperer_donnees(id_nuit):
    # lecture du CSV
    print("LECTURE DU CSV")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin_csv = os.path.join(base_dir, "raw", "traite", f"signal-psg-patient-{id_nuit}-nuit-{id_nuit}.csv")
    df_capteur = pd.read_csv(chemin_csv)
    print("LE CSV A BIEN ETE LU")
    # lecture des événements (MySQL)
    conn = mysql.connector.connect(
        host=os.environ.get("host"),
        user=os.environ.get("user"),
        password=os.environ.get("password"),
        database=os.environ.get("database")
    )
    query = f"SELECT * FROM evenement_respiratoire WHERE id_nuit = {id_nuit}"
    df_events = pd.read_sql(query, conn)
    conn.close()



    return df_capteur, df_events