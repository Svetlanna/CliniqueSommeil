import pandas as pd

def calculer_indicateurs(df_capteur, df_events):

    stats = {
        "spo2_min": df_capteur['spo2'].min(),
        "spo2_moy": df_capteur['spo2'].mean(),
        "spo2_mediane": df_capteur['spo2'].median(),

    }

    #print(df_events[''])
    #print(df_capteur['spo2'])

    return stats