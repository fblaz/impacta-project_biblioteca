# DDL - Camada de manipulação da tabela #

import sqlite3 as sql

con = sql.connect('library.db')
cursor = con.cursor()
cursor.execute('DROP TABLE IF EXISTS books')

sql = '''
CREATE TABLE "books" (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME TEXT,
AUTHOR TEXT,
IS_AVAILABLE BOOLEAN
)
'''

cursor.execute(sql)
con.commit()
con.close()