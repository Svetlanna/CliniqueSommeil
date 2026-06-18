import sqlite3
import os


def sauvegarder_resultats(indicateurs, id_nuit):
    # Chemin vers le dossier racine du projet
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'datalake.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Création de la table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS curated_nuit (
        id_curated INTEGER PRIMARY KEY AUTOINCREMENT,
        id_nuit INTEGER NOT NULL,
        spo2_min REAL, spo2_moy REAL, spo2_mediane REAL,
        nb_apnees INTEGER, nb_hypopnees INTEGER, nb_rera INTEGER,
        nb_microeveils INTEGER, dureehypoxiemin REAL,
        position_dominante TEXT, decibels_max REAL,
        decibels_moy REAL, nbronflementsforts INTEGER
    );
    """)

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

    # Vérification après insertion
    cursor.execute("SELECT COUNT(*) FROM curated_nuit WHERE id_nuit = ?", (id_nuit,))
    count = cursor.fetchone()[0]
    print(f"(load.py)DEBUG: {count} ligne(s) trouvée(s) pour la nuit {id_nuit} dans {db_path}")

    conn.close()