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

cursor.execute(sql)
con.commit()
con.close()
