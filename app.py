from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3 as sql

from helpers import fetch_all_books, fetch_book, fetch_user, map_book, rent, return_book, show_user_books

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Rota para exibir a página inicial/página de login

@app.route('/', methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = fetch_user(request.form['name'], request.form['password'])
        books = fetch_all_books()

        if len(user) == 0:
            session.pop('_flashes', None)
            flash('Login ou senha inválido(a)!')
            return redirect(url_for('login'))
        else:
            session['username'] = user['name']
            session['user_id'] = user['id']
            return render_template('book/books.html', books=books)
    
    return render_template('login/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/books")
def home():
    books = fetch_all_books()
    return render_template('book/books.html', books=books)

# Rota para exibir um livro específico

@app.route("/books/<int:id>")
def get_book(id):
    book_info = fetch_book(id)
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

# Rota para atualizar um livro específico

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

@app.route('/rent_book/<int:id>', methods=['GET', 'POST'])
def rent_book(id):
    book = fetch_book(id)
    if request.method == 'POST':
        user_id = session["user_id"]
        if rent(user_id, id):
            session.pop('_flashes', None)
            flash("Livro alugado com sucesso!")
            rents = show_user_books()
            return render_template('login/user.html', rents=rents)
        else:
            session.pop('_flashes', None)
            flash("Livro indisponível para locação")
            rents = show_user_books()
            return render_template('login/user.html', rents=rents)
    
    return render_template('book/rent_book.html', book=book)

@app.route('/rents', methods=['GET'])
def rented_books():
    rents = show_user_books()

    return render_template('login/user.html', rents=rents)

@app.route('/return_book/<int:id>', methods=['GET'])
def return_rented_book(id):
    user_id = session["user_id"]
    
    if return_book(user_id, id):
        session.pop('_flashes', None)
        flash("Livro devolvido com sucesso!")
        rents = show_user_books()
        return render_template('login/user.html', rents=rents)
    else:
        session.pop('_flashes', None)
        flash("Erro na devolução do livro!")
        rents = show_user_books()
        return render_template('login/user.html', rents=rents)

if __name__ == "__main__":
    app.run(debug=True)