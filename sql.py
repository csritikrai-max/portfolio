import sqlite3

conn = sqlite3.connect('contact.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM contacts")
print(cursor.fetchall())


conn.close()
