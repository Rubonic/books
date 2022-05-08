from types import ClassMethodDescriptorType
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

db = 'books_schema'

class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO books (title, num_of_pages, created_at, updated_at) VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW())"

        result = connectToMySQL(db).query_db(query, data)
        return result


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books"

        results = connectToMySQL(db).query_db(query)

        books = []

        for book in results:
            books.append(cls(book))
        return books


    @classmethod
    def get_all_favorites(cls, data):
        query1 = "SELECT * FROM books JOIN favorites ON books.id = favorites.book_id JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(book_id)s"
        query2 = "SELECT * FROM books WHERE id = %(book_id)s"

        result1 = connectToMySQL(db).query_db(query1, data)
        result2 = connectToMySQL(db).query_db(query2, data)

        book = cls(result2[0])

        for row in result1:
            author_data = {
                'id' : row['authors.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'created_at' : 'NOW()',
                'updated_at' : 'NOW()'
            }

            book.authors.append(author.Author(author_data))

        return book


    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (book_id, author_id) VALUES (%(book_id)s, %(author_id)s);"

        return connectToMySQL(db).query_db(query, data)

