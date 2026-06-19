import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "datalake.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DELETE FROM curated_nuit")
cursor.execute("DELETE FROM raw_capteur")

conn.commit()
conn.close()

print("Tables curated_nuit et raw_capteur vidées.")