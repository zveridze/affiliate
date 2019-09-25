import sqlite3


def check_db_schema(specific_db_name):
    conn = sqlite3.connect(specific_db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    db_schema = cursor.fetchall()
    cursor.close()
    conn.close()
    return db_schema

