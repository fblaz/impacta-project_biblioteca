# DDL - Camada de manipulação da tabela #

import sqlite3 as sql

# Criar tabela de livros

con = sql.connect('library.db')
cursor = con.cursor()
cursor.execute('DROP TABLE IF EXISTS books')

sql_create_books = '''
CREATE TABLE "books" (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME TEXT,
AUTHOR TEXT,
IS_AVAILABLE BOOLEAN
)
'''

# Criar tabela de usuários

sql_create_user = '''
CREATE TABLE "user" (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME TEXT,
PASSWORD VARCHAR
)
'''

# Criar tabela de conexão usuário/livro

sql_create_user_book_link = '''CREATE TABLE "rent"
(id INTEGER PRIMARY KEY,
 user_id INTEGER,
 book_id INTEGER,
 date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (user_id) REFERENCES user(id),
 FOREIGN KEY (book_id) REFERENCES books(id))
'''

cursor.execute(sql_create_books)
cursor.execute(sql_create_user)
cursor.execute(sql_create_user_book_link)

con.commit()
con.close()