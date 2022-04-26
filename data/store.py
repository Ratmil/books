from data.dbbookstore import DBBookStore
from data.openapi import OpenApiStore
from models.models import Book, Comment
from data.errors import *
import configparser


DEFAULT_API_URL = "https://openlibrary.org"
DEFAULT_DB = "db/books.db"

class StoreError(Exception):
    def __init__(self, msg: str):
        self.msg = msg



#
# Class to manage information about books.
# Get and save book info, comments, authors
# 
class BookStore:
    __instance = None
    
    def __init__(self):
        self._dbname = DEFAULT_DB
        self._apiUrl = DEFAULT_API_URL
        config = configparser.RawConfigParser()
        config.read('config.cfg')
        if 'API' in config.sections():
            api_config = dict(config.items('API'))
            if 'api_url' in api_config:
                self._apiUrl = api_config['api_url']

    def _getLocalStore(self):
        return DBBookStore.getInstance(self._dbname)

    def _getRemoteStore(self):
        return OpenApiStore.getInstance(self._apiUrl)
        
    # Returns single instance of this class
    @staticmethod
    def getInstance():
        if not BookStore.__instance:
            BookStore.__instance = BookStore()
        return BookStore.__instance

    # Returns info about book by given ISBN
    def getBookByISBN(self, isbn: str):
        book = self._getLocalStore().getBookByISBN(isbn)
        if not book:
            book = self._getRemoteStore().getBookByISBN(isbn)
        return book

    # Returns info about list of books by given ISBN
    def getBooksByISBN(self, isbns: str):
        books = self._getLocalStore().getBooksByISBNs(isbns)
        isbn_list = isbns.split(",")
        isbns_from_local = [book.isbn for book in books]
        missing_isbns = list(set(isbn_list) - set(isbns_from_local))
        if len(missing_isbns) > 0:
            remote_books = self._getRemoteStore().getBooksByISBN(",".join(missing_isbns))
            if remote_books:
                books.extend(remote_books)
        return books

    # Returns a list of books search by title
    def searchByTitle(self, searchText: str, limit: int = 100):
        local_store = self._getLocalStore()
        local_books = local_store.searchByTitle(searchText, limit)
        remote_store = self._getRemoteStore()
        new_limit = limit
        if local_books:
            new_limit -= len(local_books)
        remote_books = remote_store.searchByTitle(searchText, new_limit) or []
        result = []
        if local_books:
            result.extend(local_books)
        if remote_books:
            result.extend(remote_books)
        return result


    def saveBook(self, book: Book):
        return self._getLocalStore().saveBook(book)

    def updateComment(self, isbn: str, comment: Comment):
        return self._getLocalStore().updateComment(isbn, comment)

    def saveComment(self, isbn: str, comment: Comment):
        local_store = self._getLocalStore()
        book = local_store.getBookByISBN(isbn)
        if not book:
            book = self._getRemoteStore().getBookByISBN(isbn)
        if book:
            return local_store.saveComment(isbn, comment)
        else:
            return False

    def getComments(self, isbn: str):
        local_store = self._getLocalStore()
        book = local_store.getBookByISBN(isbn)
        if not book:
            book = self._getRemoteStore().getBookByISBN(isbn)
        if book:
            return self._getLocalStore().getComments(isbn)
        else:
            return False

    def deleteComment(self, isbn: str, comment_id: int):
        return self._getLocalStore().deleteComment(isbn, comment_id)

    def validateBook(self, book: Book):
        if not book.title or len(book.title) < 3:
            return ERROR_INVALID_BOOK_TITLE
        if not book.isbn or len(book.isbn) < 1:
            return ERROR_INVALID_BOOK_ISBN
        return ERROR_OK

    def validateComment(self, comment: Comment):
        if not comment.user_name or len(comment.user_name) < 2:
            return ERROR_INVALID_USER_NAME
        if not comment.subject or len(comment.subject) < 1:
            return ERROR_INVALID_COMMENT_SUBJECT
        if not comment.text or len(comment.text) < 5:
            return ERROR_INVALID_COMMENT_TEXT
        return ERROR_OK
