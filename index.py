from etl.extract import recuperer_donnees
from etl.transform import calculer_indicateurs
from etl.load import sauvegarder_resultats


def run_pipeline(id_nuit):
    queries_response : dict = recuperer_donnees(id_nuit)
    df_capteur = queries_response['df_capteur']
    df_event = queries_response['df_events']
    print(f"Étape 1 : Extraction : \n    {len(df_capteur)} lignes lues dans le CSV.\n    {queries_response['nbr_events'][0]} lignes lues dans la base MySQL.")

    # 2. Transformation
    print("Étape 2 : Calcul des indicateurs...")
    indicateurs = calculer_indicateurs(
        queries_response['df_capteur'],
        queries_response['df_events'],
        queries_response['nbapnees'],
        queries_response['nbhypopnees'],
        queries_response['nbrera'],
        queries_response['nbr_events']  # Assurez-vous que cette clé est bien dans votre dict dans extract.py
    )


    # 3. Chargement
    print("Étape 3 : Sauvegarde dans le Datalake...")
    sauvegarder_resultats(indicateurs, id_nuit,df_capteur)


run_pipeline(2)