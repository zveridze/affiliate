import sqlite3


def do_sql(specific_db_name, specific_sql):
    conn = sqlite3.connect(specific_db_name)
    cursor = conn.cursor()
    cursor.execute(specific_sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
