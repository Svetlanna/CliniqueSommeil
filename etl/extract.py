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
        port=os.environ.get("port"),
        password=os.environ.get("password"),
        database=os.environ.get("database")
    )

    cur = conn.cursor(buffered=True)
    query = f'SELECT * FROM evenement_respiratoire WHERE id_nuit = {id_nuit}'
    cur.execute(query)
    df_events = cur.fetchall()

    # Des bugs apparaissent lorsque chaque query est execute séparement
    # recours a une fnction local pour fix
    def call_proc(cursor, proc):
        cursor.execute(f"CALL {proc};")
        result = cursor.fetchone()
        while cursor.nextset() is not None:
            pass
        return result

    nbapnees = call_proc(cur, "clinique2nuitsv2.sp_compteur_apnees()")
    nbhypopnees = call_proc(cur, "clinique2nuitsv2.sp_compteur_hypopnae()")
    nbrera = call_proc(cur, "clinique2nuitsv2.sp_compteur_rera()")
    nbr_events = call_proc(cur, "clinique2nuitsv2.sp_compteur_all()")

    queries_response = {
        'df_capteur': df_capteur,
        'df_events': df_events,
        'nbapnees': nbapnees,
        'nbhypopnees': nbhypopnees,
        'nbrera': nbrera,
        'nbr_events': nbr_events,
    }
    print(nbhypopnees[0])
    conn.close()

    return queries_response