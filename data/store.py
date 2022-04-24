from data.dbbookstore import DBBookStore
from data.openapi import OpenApiStore
import configparser


DEFAULT_API_URL = "https://openlibrary.org"
DEFAULT_DB = "db/books.db"

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

    #Returns info about book by given ISBN
    def getBookByISBN(self, isbn: str):
        book = self._getLocalStore().getBookByISBN(isbn)
        if not book:
            book = self._getRemoteStore().getBookByISBN(isbn)
        return book