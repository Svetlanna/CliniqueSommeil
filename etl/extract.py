import pandas as pd
import mysql.connector

def recuperer_donnees(id_nuit):
    # lecture du CSV
    chemin_csv = f"/signal-psg-patient-{id_nuit}-nuit-{id_nuit}.csv"
    df_capteur = pd.read_csv(chemin_csv)


    # lecture des événements (MySQL)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="clinique2nuitsv2"
    )
    query = f"SELECT * FROM evenement_respiratoire WHERE id_nuit = {id_nuit}"
    df_events = pd.read_sql(query, conn)
    conn.close()




    return df_capteur, df_events