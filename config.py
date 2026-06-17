import csv
import mysql.connector
import sqlite3
import matplotlib.pyplot as plt



cnx = mysql.connector.connect(
    host="localhost",
    port=3333,
    user="root",
    password="root",
    database="patients"
)
cur = cnx.cursor(dictionary=True)