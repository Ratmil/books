from fastapi import FastAPI, Response, status
from data.openapi import OpenApiStore

app = FastAPI()
bookStore = OpenApiStore.getInstance()

# Returns info about one book by ISBN
@app.get("/book/{isbn}")
def getBookByISBN(isbn: str, response: Response):
    book = bookStore.getBookByISBN(isbn)
    if not book:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return book

# Returns info about list of books by ISBN
@app.get("/books/{isbns}")
def getBooksByISBN(isbns: str, response: Response):
    books = bookStore.getBooksByISBN(isbns)
    if not books:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return books

# Returns results from a search by book title
@app.get("/bookssearch")
def getBooksBySearchText(text: str, limit: int = 100):
    return bookStore.searchByTitle(text, limit)
