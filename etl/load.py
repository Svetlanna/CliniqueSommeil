import sqlite3
import os
import matplotlib.pyplot as plt
import shutil

def creer_tables_datalake():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'datalake.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_capteur (
        id_raw              INTEGER PRIMARY KEY AUTOINCREMENT,
        id_nuit             INTEGER NOT NULL,
        timestamp_sec       INTEGER NOT NULL,
        spo2                REAL,
        debitnasalpct       REAL,
        effortthoraciquepct REAL,
        position            TEXT,
        ronflements_db      REAL,
        flagevenement       INTEGER CHECK (flagevenement IN (0,1))
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS curated_nuit (
        id_curated        INTEGER PRIMARY KEY AUTOINCREMENT,
        id_nuit           INTEGER NOT NULL,
        spo2_min          REAL,
        spo2_moy          REAL,
        spo2_mediane      REAL,
        nb_apnees         INTEGER,
        nb_hypopnees      INTEGER,
        nb_rera           INTEGER,
        nb_microeveils    INTEGER,
        dureehypoxiemin   REAL,
        position_dominante TEXT,
        decibels_max      REAL,
        decibels_moy      REAL,
        nbronflementsforts INTEGER
    );
    """)

    conn.commit()
    conn.close()


def charger_raw_capteur(df_capteur, id_nuit):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'datalake.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    rows = [
        (
            id_nuit,
            int(row['timestamp_sec']),
            row.get('spo2'),
            row.get('debitnasalpct'),
            row.get('effortthoraciquepct'),
            row.get('position'),
            row.get('ronflements_db'),
            int(row['flag_evenement']) if row.get('flag_evenement') is not None else None,
        )
        for _, row in df_capteur.iterrows()
    ]

    cursor.executemany("""
    INSERT INTO raw_capteur (id_nuit, timestamp_sec, spo2, debitnasalpct, effortthoraciquepct, position, ronflements_db, flagevenement)
    VALUES (?,?,?,?,?,?,?,?)
    """, rows)

    conn.commit()
    print(f"(load.py) {len(rows)} lignes insérées dans raw_capteur pour la nuit {id_nuit}")
    conn.close()


def copier_csv_vers_traite(id_nuit):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nom_fichier = f"signal-psg-patient-{id_nuit}-nuit-{id_nuit}.csv"
    src = os.path.join(base_dir, "raw", nom_fichier)
    dst_dir = os.path.join(base_dir, "raw", "traite")
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy2(src, dst_dir)
    print(f"(load.py) CSV nuit {id_nuit} copié dans raw/traite/")


def sauvegarder_resultats(indicateurs, id_nuit, df_capteur):
    # Chemin vers le dossier racine du projet
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'datalake.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    INSERT INTO curated_nuit (
        id_nuit, spo2_min, spo2_moy, spo2_mediane, nb_apnees, 
        nb_hypopnees, nb_rera, nb_microeveils, dureehypoxiemin, 
        position_dominante, decibels_max, decibels_moy, nbronflementsforts
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    data = (
        id_nuit,
        indicateurs.get("spo2_min", 0.0),
        indicateurs.get("spo2_moy", 0.0),
        indicateurs.get("spo2_mediane", 0.0),
        indicateurs.get("nb_apnees", 0),
        indicateurs.get("nb_hypopnees", 0),
        indicateurs.get("nb_rera", 0),
        indicateurs.get("nb_microeveils", 0),
        indicateurs.get("dureehypoxiemin", 0.0),
        indicateurs.get("position_dominante", "Inconnue"),
        indicateurs.get("decibels_max", 0.0),
        indicateurs.get("decibels_moy", 0.0),
        indicateurs.get("nbronflementsforts", 0)
    )

    cursor.execute(query, data)
    conn.commit()
    # /////////////////222222222222222222222///////////////////////////////////////
    # 2. Enregistrement des données brutes (raw_capteur)
    cursor2 = conn.cursor()

    cursor2.execute("""
           CREATE TABLE IF NOT EXISTS raw_capteur (
            id_raw INTEGER PRIMARY KEY AUTOINCREMENT,
            id_nuit INTEGER NOT NULL,
            timestamp_sec INTEGER NOT NULL,
            spo2 REAL,
            debitnasalpct REAL,
            effortthoraciquepct REAL,
            position TEXT,
            ronflements_db REAL,
            flagevenement INTEGER
           );
           """)

    query2 = """
           INSERT INTO raw_capteur (
            id_nuit, timestamp_sec, spo2, debitnasalpct,
            effortthoraciquepct, position, ronflements_db, flagevenement
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           """

    # Itération sur chaque ligne du DataFrame pour l'insertion
    for index, row in df_capteur.iterrows():
        # Construction du tuple pour la ligne courante
        data_row = (
            id_nuit,
            row['timestamp_sec'],
            row['spo2'],
            row['debit_nasal_pct'],  # Vérifiez bien le nom de la colonne
            row['effort_thoracique_pct'],
            row['position'],
            row['ronflements_db'],
            0  # Valeur par défaut pour flagevenement, à ajuster si besoin
        )
        cursor2.execute(query2, data_row)

    conn.commit()
    print(f"Sauvegarde de {len(df_capteur)} lignes dans raw_capteur effectuée.")

    # ////////////////////////222222222222222222///////////////////////////////////

    plt.figure()
    plt.plot(df_capteur.index, df_capteur['spo2'], marker='o')
    plt.xlabel("Temps")
    plt.ylabel("SpO2 ")
    plt.title(f"Évolution SpO2 - Nuit {id_nuit}")
    plt.grid(True)
    plt.savefig(f"courbe_spo2_nuit_{id_nuit}.png")
    plt.close()
    print("Courbe SpO2 sauvegardée.")

    plt.figure()
    plt.plot(df_capteur.index, df_capteur['debitnasalpct'], color='green')
    plt.xlabel("Temps")
    plt.ylabel("Débit Nasal")
    plt.title(f"Évolution Débit Nasal - Nuit {id_nuit}")
    plt.grid(True)
    plt.savefig(f"courbe_debit_nasal_nuit_{id_nuit}.png")
    plt.close()
    print("Courbe Débit Nasal sauvegardée.")

    plt.figure()
    plt.plot(df_capteur["timestamp_sec"], df_capteur["ronflements_db"], color="#9467bd", linewidth=1)
    plt.xlabel("Temps")
    plt.ylabel("Débit Nasal")
    plt.title(f"Ronflements  {id_nuit}")
    plt.grid(True)
    plt.savefig(f"ronflements{id_nuit}_vs_temps.png")
    plt.close()
    print("Courbe ronflements dB vs temps")

    cursor.execute("SELECT COUNT(*) FROM curated_nuit WHERE id_nuit = ?", (id_nuit,))
    count = cursor.fetchone()[0]
    print(f"(load.py)DEBUG: {count} ligne(s) trouvée(s) pour la nuit {id_nuit} dans {db_path}")

    conn.close()