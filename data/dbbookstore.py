import sqlite3
from contextlib import closing
from models.models import Book, Author, Comment


class DBError(Exception):
    def __init__(msg: str):
        self.msg = msg

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

    # Saves a book into database
    def saveBook(self, book: Book):
        with closing(sqlite3.connect(self._dbname)) as con, closing(con.cursor()) as cr:
            # Get book by ISBN
            query = "SELECT id FROM books WHERE isbn = ?"
            cr.execute(query, (book.isbn,))
            row = cr.fetchone()
            if row:
                book_id = row[0]
                query = "UPDATE books SET title=?, url=?, number_of_pages=? WHERE id = ?"
                cr.execute(query, (book.title, book.url or '', book.number_of_pages, book_id))
                if cr.rowcount < 1:
                    raise DBError("Error updating book")
                cr.execute("DELETE FROM books_authors WHERE book_id = ?", (book_id, ))
            else:
                query = "INSERT INTO books(isbn, title, url, number_of_pages) VALUES(?, ?, ?, ?)"
                cr.execute(query, (book.isbn, book.title, book.url or '', book.number_of_pages))
                if cr.rowcount < 1:
                    raise DBError("Error inserting book")
                book_id = cr.lastrowid
            for author in book.authors:
                author_id = self._updateAuthorByName(cr, author)
                cr.execute("INSERT INTO books_authors(book_id, author_id) VALUES(?, ?)", (book_id, author_id))
                if cr.rowcount < 1:
                    raise DBError("Error linking author to book")
            con.commit()
        return True

    # Saves a comment about a book
    def saveComment(self, isbn: str, comment: Comment):
        with closing(sqlite3.connect(self._dbname)) as con, closing(con.cursor()) as cr:
            cr.execute("INSERT INTO comments(user_name, subject, comment, book_isbn) VALUES(?, ?, ?, ?)",
                       (comment.user_name, comment.subject, comment.text, isbn))
            if cr.rowcount < 1:
                raise DBError("Error saving comment")
            comment.comment_id = cr.lastrowid
            con.commit()
            return True

    # Returns list of comments of given ISBN book
    def getComments(self, isbn: str):
        with closing(sqlite3.connect(self._dbname)) as con, closing(con.cursor()) as cr:
            cr.execute("SELECT id, user_name, subject, comment FROM comments WHERE book_isbn = ?", (isbn, ))
            rows = cr.fetchall()
            comments = []
            for row in rows:
                comment = Comment(comment_id=row[0], user_name=row[1], subject=row[2], text=row[3])
                comments.append(comment)
            return comments

    # Deletes a comment
    def deleteComment(self, isbn: str, comment_id: int):
        with closing(sqlite3.connect(self._dbname)) as con, closing(con.cursor()) as cr:
            cr.execute("DELETE FROM comments WHERE book_isbn = ? AND id = ?",
                       (isbn, comment_id))
            if cr.rowcount < 1:
                raise DBError("Error deleting comment")
            con.commit()
            return True

    def _updateAuthorByName(self, cr, author: Author):
        cr.execute("SELECT id FROM authors WHERE name = ?", (author.name, ))
        row = cr.fetchone()
        if row:
            cr.execute("UPDATE authors SET url = ? WHERE id = ?", (author.url or '', row[0]))
            if cr.rowcount < 1:
                raise DBError("Error updating author")
            return row[0]
        else:
            cr.execute("INSERT INTO authors(name, url) VALUES(?, ?)", (author.name, author.url))
            if cr.rowcount < 1:
                raise DBError("Error inserting author")
            return cr.lastrowid
