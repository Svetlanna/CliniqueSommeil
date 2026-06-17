import pandas as pd
def calculer_indicateurs(df_capteur, df_events):
    stats = {
        "spo2_min": df_capteur['spo2'].min(),
        "spo2_moy": df_capteur['spo2'].mean(),
        "spo2_mediane": df_capteur['spo2'].median(),
        "decibels_max": df_capteur['ronflements_db'].max(),
        "decibels_moy": df_capteur['ronflements_db'].mean(),
        "nbronflementsforts": int((df_capteur['ronflements_db'] > 70).sum()),
        "position_dominante": df_capteur['position'].mode()[0],
        "dureehypoxiemin": (df_capteur['spo2'] < 90).sum() * (10 / 60)
    }



    nb_apnees = len(df_events[df_events['type_evenement'].str.contains('apnée')]) * 3.5
    nb_hypopnees = len(df_events[df_events['type_evenement'] == 'hypopnée']) * 3.5
    nb_rera = len(df_events[df_events['type_evenement'] == 'RERA']) * 3.5

    stats.update({
        "nb_apnees": int(nb_apnees),
        "nb_hypopnees": int(nb_hypopnees),
        "nb_rera": int(nb_rera),
        "dureesommeilmin": 420,
        "iah": (nb_apnees + nb_hypopnees + nb_rera) / 7
    })
    print(df_events)
    return stats