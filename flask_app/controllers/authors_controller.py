from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.author import Author
from flask_app.models.book import Book


@app.route('/')
def reroute():

    return redirect('/authors')

@app.route('/authors')
def authors():


    return render_template('authors.html', authors = Author.get_all())

@app.route('/create/author', methods=['POST'])
def create_author():

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'created_at' : 'NOW()',
        'updated_at' : 'NOW()'
    }
    print("===============")
    author = Author.create(data)
    print(author)

    return redirect('/authors')


@app.route('/author/<int:author_id>')
def show_author(author_id):

    data = {
        'author_id' : author_id
    }

    return render_template('author_show.html', author = Author.get_author_favorites(data), books = Book.get_all())


@app.route('/add_favorite/<int:author_id>', methods=['POST'])
def add_favorite(author_id):

    data = {
        'book_id': request.form['fav_book'],
        'author_id' : author_id
    }

    Author.add_favorite(data)

    return redirect(f'/author/{author_id}')
