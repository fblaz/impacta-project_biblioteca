import sqlite3 as sql

# Função para buscar todos os livros cadastrados no banco de dados
def fetch_all_books():
    con = sql.connect('library.db')
    cur = con.cursor()

    cur.execute("""
    SELECT * FROM books
    """)

    books = cur.fetchall()

    books_resp = list(map(map_book, books))
    return books_resp

def fetch_book(book_id):
    con = sql.connect('library.db')
    cur = con.cursor()

    cur.execute(f"""
    SELECT * FROM books WHERE id = {book_id}
    """)

    book = cur.fetchone()
    return map_book(book)

def fetch_user(name, password):
        con = sql.connect('library.db')
        cur = con.cursor()

        print(name, password)

        query = f"SELECT * FROM user where name='{name}' and password='{password}'"
        cur.execute(query)

        user = cur.fetchone()
        if user:
            return map_user(user)
        else:
            return {}

def rent(user_id, book_id):
    con = sql.connect('library.db')
    cur = con.cursor()
    book = fetch_book(book_id)
    
    if book["is_available"] == "Sim":
        cur.execute("INSERT INTO rent (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
        cur.execute(f"UPDATE books SET is_available='0' WHERE id={book_id}")
    else:
        return False
    
    con.commit()
    con.close()

    return True

def return_book(user_id, book_id):
    con = sql.connect('library.db')
    cur = con.cursor()
    book = fetch_book(book_id)
    
    cur.execute(f"DELETE FROM rent WHERE book_id ={book_id} and user_id={user_id}")
    cur.execute(f"UPDATE books SET is_available='1' WHERE id={book_id}")
    
    con.commit()
    con.close()

    return True


def show_user_books():
    con = sql.connect('library.db')
    cur = con.cursor()
    cur.execute('''SELECT books.id, books.name, books.author, books.is_available
                 FROM user JOIN rent ON user.id=rent.user_id
                            JOIN books ON rent.book_id=books.id''')
    user_books = cur.fetchall()
    con.close()

    return list(map(map_book, set(user_books)))


# Função para mapear os dados do banco de dados para um dicionário
def map_book(book):
    return {
        "id": book[0],
        "name": book[1],
        "author": book[2],
        "is_available": "Sim" if book[3] == 1 else "Não"
    }

def map_user(user):
    return {
        "id": user[0],
        "name": user[1],
        "password": user[2],
    }