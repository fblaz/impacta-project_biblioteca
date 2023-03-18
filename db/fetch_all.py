import sqlite3 as sql

con = sql.connect('library.db')
cursor = con.cursor()

sql = '''
SELECT * FROM books
'''

cursor.execute(sql)

books = cursor.fetchall()
print(books)

con.commit()
con.close()