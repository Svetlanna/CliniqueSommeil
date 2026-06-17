import sqlite3

def sauvegarder_resultats(indicateurs, id_nuit):
    conn = sqlite3.connect('datalake.db')
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
        indicateurs['spo2_min'],
        indicateurs['spo2_moy'],
        indicateurs['spo2_mediane'],
        indicateurs['nb_apnees'],
        indicateurs['nb_hypopnees'],
        indicateurs['nb_rera'],
        0,  # nb_microeveils (pas encore dans votre dico)
        indicateurs['dureehypoxiemin'],
        indicateurs['position_dominante'],
        indicateurs['decibels_max'],
        indicateurs['decibels_moy'],
        indicateurs['nbronflementsforts']
    )

    try:
        cursor.execute(query, data)
        conn.commit()
        print(f"Succès : Données enregistrées pour la nuit {id_nuit}")
    except sqlite3.Error as e:
        print(f"Erreur SQL : {e}")
    finally:
        conn.close()

