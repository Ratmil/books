from fastapi import FastAPI, Response, status
from data.openapi import OpenApiStore

app = FastAPI()

# Returns info about one book by ISBN
@app.get("/book/{isbn}")
def getBookByISBN(isbn: str, response: Response):
    bookStore = OpenApiStore.getInstance()
    books = bookStore.getBookByISBN(isbn)
    if not books or len(books) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
    return books