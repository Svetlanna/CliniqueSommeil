from etl.extract import recuperer_donnees
from etl.transform import calculer_indicateurs
from etl.load import sauvegarder_resultats


def run_pipeline(id_nuit):
    df_capteur, data_sql = recuperer_donnees(id_nuit)
    print(f"Extraction terminée : {len(df_capteur)} lignes lues dans le CSV.")

    # 2. Transformation
    print("Étape 2 : Calcul des indicateurs...")
    indicateurs = calculer_indicateurs(df_capteur, data_sql)

    # 3. Chargement
    print("Étape 3 : Sauvegarde dans le Datalake...")
    sauvegarder_resultats(indicateurs, id_nuit)


run_pipeline(1)