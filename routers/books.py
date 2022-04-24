from fastapi import FastAPI, Response, status
from data.store import BookStore
from models.models import Book, Comment


app = FastAPI()
bookStore = BookStore.getInstance()

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

# Saves information of a book
@app.put("/book")
def saveBook(book: Book, response: Response):
    if not bookStore.saveBook(book):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return book

# Saves a comment about a book
@app.put("/book/{isbn}/comment")
def saveComment(isbn: str, comment: Comment):
    if not bookStore.saveComment(isbn, comment):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return comment

# Return list of comments
@app.get("/book/{isbn}/comments")
def getComments(isbn: str):
    return bookStore.getComments(isbn)

@app.delete("/book/{isbn}/comment/{comment_id}")
def deleteComment(isbn: str, comment_id: int):
    return bookStore.deleteComment(isbn, comment_id)