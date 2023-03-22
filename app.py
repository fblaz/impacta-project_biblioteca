from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
@app.route("/books")
def home():
    books = fetch_all_books()
    return render_template('book/books.html', books=books)

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

def fetch_all_books():
    con = sql.connect('library.db')
    cur = con.cursor()
    
    cur.execute("""   
    SELECT * FROM books
    """)
    
    books = cur.fetchall()
    
    books_resp = list(map(map_book, books))
    return books_resp

def map_book(book):
    return {
        "id": book[0],
        "name": book[1],
        "author": book[2],
        "is_available": "Yes" if book[3] == 1 else "No" 
    }
    

if __name__ == "__main__":
    app.run(debug=True)
