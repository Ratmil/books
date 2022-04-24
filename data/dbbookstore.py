import sqlite3


class DBBookStore:
    instance = None

    def __init__(self, dbname = "books.db"):
        self.dbname = dbname
        
    # Returns single instance of this class
    @staticmethod
    def getInstance():
        if not DBBookStore.instance:
            DBBookStore.instance = DBBookStore()
        return DBBookStore.instance

    #Returns info about book by given ISBN
    def getBookByISBN(self, isbn: str):
        self.conn = sqlite3.connect(self.dbname)
        cr = self.conn.cursor()
        print(isbn)
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
            return book
        return False