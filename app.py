from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Rota para exibir a página inicial
# Rota para página de login
@app.route('/', methods=['GET', 'POST'])
@app.route("/login")
def login():
    if request.method == 'POST':

        connection = sql.connect('library.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        print(name, password)

        query  = "SELECT name, password FROM user where name= '"+name+"' and password= '"+password+"'"
        cursor.execute(query)
        results = cursor.fetchall()

        books = fetch_all_books()

        if len(results) == 0:
            print("Sorry, Incorrect Credentials Provided. Try again")
        else:
            return render_template('book/books.html', books=books)
    return render_template('login/login.html')

@app.route("/books")
def home():
    books = fetch_all_books()
    return render_template('book/books.html', books=books)

# Rota para exibir um livro específico
@app.route("/books/<int:id>")
def get_book(id):
    con = sql.connect('library.db')
    cur = con.cursor()

    cur.execute(f"""
    SELECT * FROM books WHERE id = {id}
    """)

    book = cur.fetchone()
    book_info = map_book(book)
    return render_template('book/book.html', book=book_info)

# Rota para exibir o formulário de cadastro de livro
@app.route("/book_form")
def book_form():
    return render_template('book/book_form.html')

# Rota para cadastrar um novo livro
@app.route("/cadastro_livro", methods=["POST"])
def cadastrar_livro():
    try:
        nome_autor = request.form["nome-autor"]
        nome_livro = request.form["nome-livro"]

        con = sql.connect('library.db')
        cur = con.cursor()

        cur.execute(f"""
            INSERT INTO books (name, author, is_available)
            VALUES ('{nome_livro}', '{nome_autor}', 1)
        """)

        con.commit()
        flash("Livro cadastrado com sucesso!")
        return redirect(url_for('home'))

    except Exception as e:
        con.rollback()
        flash("Erro ao cadastrar livro: " + str(e))
        return redirect(url_for('book_form'))

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

# Função para mapear os dados do banco de dados para um dicionário
def map_book(book):
    return {
        "id": book[0],
        "name": book[1],
        "author": book[2],
        "is_available": "Sim" if book[3] == 1 else "Não"
    }


@app.route("/books/editar/<int:id>")
def edit_book_form(id):
    con = sql.connect('library.db')
    cur = con.cursor()

    cur.execute(f"""
    SELECT * FROM books WHERE id = {id}
    """)

    book = cur.fetchone()
    book_info = map_book(book)
    return render_template('book/edit_book.html', book=book_info)

# Rota para atualizar um livro específico

@app.route("/books/editar/<int:id>", methods=["POST"])
def edit_book(id):
    try:
        nome_autor = request.form["nome-autor"]
        nome_livro = request.form["nome-livro"]

        con = sql.connect('library.db')
        cur = con.cursor()

        cur.execute(f"""
            UPDATE books SET name='{nome_livro}', author='{nome_autor}' WHERE id={id}
        """)

        con.commit()
        flash("Livro atualizado com sucesso!")
        return redirect(url_for('get_book', id=id))

    except Exception as e:
        con.rollback()
        flash("Erro ao atualizar livro: " + str(e))
        return redirect(url_for('edit_book_form', id=id))

# Rota para excluir um livro específico

@app.route('/delete_book/<int:id>', methods=['GET', 'POST'])
def delete_book(id):
    con = sql.connect('library.db')
    cur = con.cursor()

    if request.method == 'POST':
        cur.execute(f"DELETE FROM books WHERE id = {id}")
        con.commit()
        flash("Livro deletado com sucesso!")
        return redirect(url_for('home'))

    cur.execute(f"SELECT * FROM books WHERE id = {id}")
    book = cur.fetchone()
    book_info = map_book(book)

    return render_template('book/delete_book.html', book=book_info)

if __name__ == "__main__":
    app.run(debug=True)