import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute(
    "CREATE TABLE Companies(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, revenue INTEGER, employees INTEGER)")
cur.execute('INSERT INTO Companies(name, revenue, employees) VALUES(?, ?, ?)', ('apple', '260', '137000'))
cur.execute('INSERT INTO Companies(name, revenue, employees) VALUES(?, ?, ?)', ('samsung', '197', '287000'))
cur.execute('INSERT INTO Companies(name, revenue, employees) VALUES(?, ?, ?)', ('alphabet', '161', '118899'))

conn.commit()
cur.close()