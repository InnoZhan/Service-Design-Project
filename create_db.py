import sqlite3

con = sqlite3.connect('barber.db')

cur = con.cursor()

# cur.execute('''CREATE TABLE feedback
#                (id INTEGER PRIMARY KEY, employee TEXT, rate REAL, service TEXT, phone TEXT, feedback TEXT, alias TEXT, timedate TEXT)''')

cur.execute("DELETE FROM feedback WHERE service = 'Blowjob'")

# cur.execute('DROP TABLE feedback')

# rows = cur.execute("SELECT * FROM feedback")

# for row in rows:
#     print(row)

con.commit()