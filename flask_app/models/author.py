from types import ClassMethodDescriptorType
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

db = 'books_schema'

class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []


    @classmethod
    def create(cls, data):
        query = "INSERT INTO authors (first_name, last_name, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, NOW(), NOW())"

        print('================')
        result = connectToMySQL(db).query_db(query, data)
        print('+++++++++++++++++')
        print(result)
        return result


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors"

        results = connectToMySQL(db).query_db(query)

        authors = []

        for author in results:
            authors.append(cls(author))
        return authors
    

    @classmethod
    def get_author_favorites(cls, data):
        query1 = "SELECT * FROM authors JOIN favorites ON favorites.author_id = authors.id JOIN books ON favorites.book_id = books.id WHERE authors.id = %(author_id)s"
        query2 = "SELECT * FROM authors WHERE id = %(author_id)s"

        result1 = connectToMySQL(db).query_db(query1, data)
        result2 = connectToMySQL(db).query_db(query2, data)

        author = cls(result2[0])
        
        for row in result1:
            book_data = {
                'id' : row['books.id'],
                'title' : row['title'],
                'num_of_pages' : row['num_of_pages'],
                'created_at' : 'NOW()',
                'updated_at' : 'NOW()',
            }

            author.books.append(book.Book(book_data))

        return author

    
    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (book_id, author_id) VALUES (%(book_id)s, %(author_id)s)"

        return connectToMySQL(db).query_db(query, data)



            
        





        
        