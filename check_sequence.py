import sqlite3

conn = sqlite3.connect('yumpooma.db')
c = conn.cursor()
c.execute('SELECT name, seq FROM sqlite_sequence')
print(c.fetchall())
