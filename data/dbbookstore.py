import sqlite3
from contextlib import closing


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

    #Returns info about book by given ISBN
    def getBookByISBN(self, isbn: str):
        with closing(sqlite3.connect(self._dbname)) as con, closing(con.cursor()) as cr:
            query = "SELECT id, title, url, number_of_pages FROM books WHERE isbn = ?"
            cr.execute(query, (isbn,))
            row = cr.fetchone()
            if row:
                book = {
                    'isbn': isbn,
                    'title': row[1],
                    'url': row[2],
                    'number_of_pages': row[3]
                }
                cr.close()
                return book
        return False