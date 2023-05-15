import sqlite3 as sql

con = sql.connect('library.db')
cursor = con.cursor()

sql = '''
INSERT INTO books (NAME, AUTHOR, IS_AVAILABLE) VALUES 
    ('A Arte da Guerra', 'TSU, Sun', 1),
    ('O Código da Vinci', 'BROWN, Dan',1),
    ('O Pequeno Príncipe', 'DE SAINT-EXUPERÝ, Antoine', 1),
    ('O Senhor dos Anéis', 'TOLKIEN, J. R. R.', 0),
    ('Misto Quente', 'BUKOWSKI, Charles', 0)
'''

# Tabela de usuários
sql_user = '''
INSERT INTO user (NAME, PASSWORD) VALUES 
    ('Thays', '1234'),
    ('Victor', '1234'),
    ('Fabio', '1234')
'''

cursor.execute(sql)
cursor.execute(sql_user)
con.commit()
con.close()
