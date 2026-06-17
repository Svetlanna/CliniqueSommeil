import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

def extract_data(csv_path, sql_query):
    # Lecture du CSV
    df = pd.read_csv(csv_path)



    conn = sqlite3.connect('clinique2nuitsv2.sql')
    df_events = pd.read_sql(sql_query, conn)
    conn.close()
    return df, df_events

def transform_data(df, df_events):

    stats = {
        'spo2_min': df['spo2'].min(),
        'spo2_moy': df['spo2'].mean(),
        'spo2_mediane': df['spo2'].median(),
        'decibels_max': df['ronflements_db'].max(),
        'decibels_moy': df['ronflements_db'].mean(),
        'nbronflementsforts': (df['ronflements_db'] > 70).sum(),
        'position_dominante': df['position'].mode()[0],
        'dureehypoxiemin': (df[df['spo2'] < 90].shape[0] * 10) / 60 # 1 ligne = 10s
    }
    # ... calculs basés sur df_events ...
    return stats

def load_to_datalake(stats, table_name, db_path='datalake.db'):
    # Logique d'insertion dans SQLite
    pass