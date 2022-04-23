import requests
from requests.exceptions import HTTPError


#Class to get and save info about books
class OpenApiStore:
    instance = None
    def __init__(self, url = "https://openlibrary.org/api"):
        self.serverURL = url


    # Returns single instance of this class
    @staticmethod
    def getInstance():
        if not OpenApiStore.instance:
            OpenApiStore.instance = OpenApiStore()
        return OpenApiStore.instance

    #Returns info about book by given ISBN
    def getBookByISBN(self, isbn: str):
        response = requests.get("%s/books/?bibkeys=ISBN:%s&format=json&jscmd=data" % (
            self.serverURL, requests.utils.quote(isbn)))
        if response.status_code == 200:
            data = response.json()
            if len(data) > 0:
                books = []
                # Select what fields to return
                fields = ['title', 'url', 'number_of_pages', 'authors']
                for key in data:
                    isbn = key.split(":")[1] if ":" in key else key
                    book_data = data[key]
                    book = {
                        'ISBN': isbn,
                    }
                    for field in fields:
                        book[field] = book_data[field]
                    books.append(book)
                return books
        return False