import requests
from requests.exceptions import HTTPError


#Class to get and save info about books
class OpenApiStore:
    __instance = None
    
    def __init__(self, url = "https://openlibrary.org"):
        self._serverURL = url


    # Returns single instance of this class
    @staticmethod
    def getInstance(url = "https://openlibrary.org"):
        if not OpenApiStore.__instance:
            OpenApiStore.__instance = OpenApiStore(url)
        return OpenApiStore.__instance

    #Returns info about book by given ISBN
    def getBookByISBN(self, isbn: str):
        response = requests.get("%s/api/books/?bibkeys=ISBN:%s&format=json&jscmd=data" % (
            self._serverURL, requests.utils.quote(isbn)))
        if response.status_code == 200:
            books = self._parseBooksResponse(response, max_count=1)
            if len(books) > 0:
                return books[0]
        return False

    #Returns info about books given isbn
    def getBooksByISBN(self, isbns):
        isbn_list = isbns.split(",")
        bibKeys = ",".join(["ISBN:%s" % requests.utils.quote(isbn) for isbn in isbn_list])
        response = requests.get("%s/api/books/?bibkeys=%s&format=json&jscmd=data" % (
            self._serverURL, bibKeys))
        if response.status_code == 200:
            books = self._parseBooksResponse(response)
            return books
        return False

    #Returns results from a search by book title
    def searchByTitle(self, text:str, limit: int = 100):
        response = requests.get("%s/search.json?title=%s&limit=%s" % (
            self._serverURL, requests.utils.quote(text), limit))
        data = response.json()
        results = []
        for doc in data["docs"]:
            print(doc.keys())
            title = doc["title"]
            isbns = doc.get("isbn", [])
            results.append({
                'title': title,
                'isbns': isbns
            })
        return results


    def _parseBooksResponse(self, response, max_count = 0):
        data = response.json()
        books = []
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
            if max_count > 0 and len(books) >= max_count:
                break
        return books