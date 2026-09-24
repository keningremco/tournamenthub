import mysql.connector
import os

def get_db_connection():
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


    cursor = db.cursor(dictionary=True)

    return db, cursor