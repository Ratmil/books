from data.dbbookstore import DBBookStore
from data.openapi import OpenApiStore


class BookStore:
    instance = None
    
    def __init__(self, dbname = "db/books.db", api="https://openlibrary.org"):
        self.dbstore = DBBookStore(dbname)
        self.apistore = OpenApiStore(api)
        
    # Returns single instance of this class
    @staticmethod
    def getInstance():
        if not BookStore.instance:
            BookStore.instance = BookStore()
        return BookStore.instance

    #Returns info about book by given ISBN
    def getBookByISBN(self, isbn: str):
        book = self.dbstore.getBookByISBN(isbn)
        if not book:
            book = self.apistore.getBookByISBN(isbn)
        return book