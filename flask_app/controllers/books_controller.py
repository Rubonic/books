from msvcrt import kbhit
from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.book import Book
from flask_app.models.author import Author


@app.route('/books')
def books():    

    return render_template('books.html', books = Book.get_all())


@app.route('/create/book', methods=['POST'])
def create_book():

    data = {
        'title' : request.form['title'],
        'num_of_pages' : request.form['num_of_pages'],
        'created_at' : 'NOW()',
        'updated_at' : 'NOW()'
    }

    book = Book.create(data)

    return redirect('/books')


@app.route('/book/<int:book_id>')
def book_show(book_id):

    data = {
        'book_id' : book_id
    }

    book = Book.get_all_favorites(data)

    return render_template('book_show.html.', book = book, authors= Author.get_all())


@app.route('/add_favorite_to_book/<int:book_id>', methods=['POST'])
def add_favorite_to_book(book_id):
    
    data = {
        'author_id': request.form['author'],
        'book_id' : book_id
    }

    Book.add_favorite(data)

    return redirect(f'/book/{book_id}')
