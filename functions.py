import sqlite3


def execute_in_sqlite(specific_db_name, specific_sql):
    conn = sqlite3.connect(specific_db_name)
    cursor = conn.cursor()
    cursor.execute(specific_sql)
    cursor.close()
    conn.commit()
    conn.close()


def return_from_sqlite(specific_db_name, specific_sql):
    conn = sqlite3.connect(specific_db_name)
    cursor = conn.cursor()
    cursor.execute(specific_sql)
    fetchalled = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return fetchalled
