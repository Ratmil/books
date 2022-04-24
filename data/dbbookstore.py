import sqlite3
from contextlib import closing
from models.models import Book, Author


class DBBookStore:
    __instance = None

    def __init__(self, dbname = "books.db"):
        self._dbname = dbname
        
    # Returns single instance of this class
    @staticmethod
    def getInstance(dbname = "books.db"):
        if not DBBookStore.__instance:
            DBBookStore.__instance = DBBookStore(dbname)
        return DBBookStore.__instance

    # Returns info about book by given ISBN
    def getBookByISBN(self, isbn: str):
        with closing(sqlite3.connect(self._dbname)) as con, closing(con.cursor()) as cr:
            # Get book by ISBN
            query = "SELECT id, title, url, number_of_pages FROM books WHERE isbn = ?"
            cr.execute(query, (isbn,))
            row = cr.fetchone()
            if row:
                book = Book(isbn = isbn, title=row[1], url=row[2], number_of_pages=row[3])
                query = """SELECT authors.id, authors.name, authors.url
                    FROM books_authors 
                    INNER JOIN authors ON books_authors.author_id = authors.id
                    WHERE books_authors.book_id = ?"""
                cr.execute(query, (row[0],))
                rows = cr.fetchall()
                authors = []
                for row in rows:
                    author = Author(name=row[1], url=row[2])
                    authors.append(author)
                book.authors = authors
                return book
            return False

    # Returns list of books by given ISBNs separated by commas
    def getBooksByISBNs(self, isbns: str):
        isbn_list = isbns.split(",")
        with closing(sqlite3.connect(self._dbname)) as con, closing(con.cursor()) as cr:
            # Get book by ISBNs
            params = ",".join(["?"] * len(isbn_list))
            query = "SELECT id, isbn, title, url, number_of_pages FROM books WHERE isbn IN (%s)" % params
            cr.execute(query, isbn_list)
            rows = cr.fetchall()
            books = []
            for row in rows:
                book = Book(isbn = row[1], title=row[2], url=row[3], number_of_pages=row[4])
                query = """SELECT authors.id, authors.name, authors.url
                    FROM books_authors 
                    INNER JOIN authors ON books_authors.author_id = authors.id
                    WHERE books_authors.book_id = ?"""
                cr.execute(query, (row[0],))
                author_rows = cr.fetchall()
                authors = []
                for author_row in author_rows:
                    author = Author(name=author_row[1], url=author_row[2])
                    authors.append(author)
                book.authors = authors
                books.append(book)
            return books

