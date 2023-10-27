import sqlite3

def sql():
    conn = sqlite3.connect('database/data.db')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id integer primary key not null, name varchar, films varchar)')
    conn.commit()
    cur.close()
    conn.close()



