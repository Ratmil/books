from fastapi import FastAPI, Response, status
from data.store import BookStore
from models.models import Book, Comment


app = FastAPI(
    title="Books API",
    description="API to manage book info"
)
bookStore = BookStore.getInstance()

# Returns info about one book by ISBN
@app.get("/book/{isbn}")
def getBookByISBN(isbn: str, response: Response):
    """
    ### Returns info about the book
    - **isbn**: ISBN to search books by
    """
    book = bookStore.getBookByISBN(isbn)
    if not book:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return book

# Returns info about list of books by ISBN
@app.get("/books/{isbns}")
def getBooksByISBN(isbns: str, response: Response):
    """
    ### Returns list of books matched by ISBN
    - **isbns**: String containing comma separated list of ISBN to search by
    """
    books = bookStore.getBooksByISBN(isbns)
    if not books:
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return books

@app.get("/search_books")
def searchBooks(title: str, limit: int = 100):
    """
    Returns a search result of books by title
    """
    books = bookStore.searchByTitle(title, limit)
    return books

# Saves information of a book
@app.put("/book")
def saveBook(book: Book, response: Response):
    """
    ### Saves book info
    """
    if not bookStore.saveBook(book):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return book

# Saves a comment about a book
@app.put("/book/{isbn}/comment")
def saveComment(isbn: str, comment: Comment, response: Response):
    """
    ### Adds a comment to a book
    - **isbn**: ISBN of book where comment will be added
    """
    if not bookStore.saveComment(isbn, comment):
        response.status_code = status.HTTP_404_NOT_FOUND
    else:
        return comment

@app.post("/book/{isbn}/comment")
def updateComment(isbn: str, comment: Comment, response: Response):
    """
    ### Updates a comment to a book
    - **isbn**: ISBN of book where comment will be added
    - **comment**: Comment about the book
    """
    if bookStore.updateComment(isbn, comment):
        return comment
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

# Return list of comments
@app.get("/book/{isbn}/comments")
def getComments(isbn: str):
    """
    ### Returns list of comments
    - **isbn**: ISBN of book to get comments
    
    """
    return bookStore.getComments(isbn)

# Deletes a comment from a book
@app.delete("/book/{isbn}/comment/{comment_id}")
def deleteComment(isbn: str, comment_id: int, response: Response):
    """
    ### Deletes a comment
    - **isbn**: ISBN of book to get comments
    - **comment_id**: Id of comment to delete
    """
    if bookStore.deleteComment(isbn, comment_id):
        return True
    else:
        response.status_code = status.HTTP_404_NOT_FOUND