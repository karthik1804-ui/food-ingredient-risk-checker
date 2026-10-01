import sqlite3

conn = sqlite3.connect("additives.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM additives LIMIT 5")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()