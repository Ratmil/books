from fastapi import FastAPI, Response, status
from data.store import BookStore
from models.models import Book, Comment
from data.errors import *


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
    try:
        book = bookStore.getBookByISBN(isbn)
        if not book:
            response.status_code = status.HTTP_404_NOT_FOUND
            return getErrorMsg(ERROR_BOOK_NOT_FOUND)
        else:
            return book
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return getErrorMsg(ERROR_UNKNOWN, str(e))

# Returns info about list of books by ISBN
@app.get("/books/{isbns}")
def getBooksByISBN(isbns: str, response: Response):
    """
    ### Returns list of books matched by ISBN
    - **isbns**: String containing comma separated list of ISBN to search by
    """
    try:
        books = bookStore.getBooksByISBN(isbns)
        if not books:
            response.status_code = status.HTTP_404_NOT_FOUND
            return getErrorMsg(ERROR_BOOK_NOT_FOUND)
        else:
            return books
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return getErrorMsg(ERROR_UNKNOWN, str(e))

@app.get("/search_books")
def searchBooks(title: str, response: Response, limit: int = 100):
    """
    Returns a search result of books by title
    """
    try:
        books = bookStore.searchByTitle(title, limit)
        return books
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return getErrorMsg(ERROR_UNKNOWN, str(e))

# Saves information of a book
@app.put("/book")
def saveBook(book: Book, response: Response):
    """
    ### Saves book info
    """
    try:
        validate_result = bookStore.validateBook(book)
        if validate_result != ERROR_OK:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return getErrorMsg(validate_result)
        elif not bookStore.saveBook(book):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return getErrorMsg(ERROR_SAVING_BOOK)
        else:
            return book
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return getErrorMsg(ERROR_UNKNOWN, str(e))

# Saves a comment about a book
@app.put("/book/{isbn}/comment")
def saveComment(isbn: str, comment: Comment, response: Response):
    """
    ### Adds a comment to a book
    - **isbn**: ISBN of book where comment will be added
    """
    try:
        validate_result = bookStore.validateComment(comment)
        if validate_result != ERROR_OK:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return getErrorMsg(validate_result)
        elif not bookStore.saveComment(isbn, comment):
            response.status_code = status.HTTP_404_NOT_FOUND
            return getErrorMsg(ERROR_BOOK_NOT_FOUND)
        else:
            response.status_code = status.HTTP_201_CREATED
            return comment
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return getErrorMsg(ERROR_UNKNOWN, str(e))

@app.post("/book/{isbn}/comment")
def updateComment(isbn: str, comment: Comment, response: Response):
    """
    ### Updates a comment to a book
    - **isbn**: ISBN of book where comment will be added
    - **comment**: Comment about the book
    """
    try:
        validate_result = bookStore.validateComment(comment)
        if validate_result != ERROR_OK:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return getErrorMsg(validate_result)
        elif bookStore.updateComment(isbn, comment):
            return comment
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return getErrorMsg(ERROR_BOOK_NOT_FOUND)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return getErrorMsg(ERROR_UNKNOWN, str(e))

# Return list of comments
@app.get("/book/{isbn}/comments")
def getComments(isbn: str, response: Response):
    """
    ### Returns list of comments
    - **isbn**: ISBN of book to get comments
    
    """
    try:
        comments = bookStore.getComments(isbn)
        if comments is False:
            return getErrorMsg(ERROR_BOOK_NOT_FOUND)
        else:
            return comments
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return getErrorMsg(ERROR_UNKNOWN, str(e))


# Deletes a comment from a book
@app.delete("/book/{isbn}/comment/{comment_id}")
def deleteComment(isbn: str, comment_id: int, response: Response):
    """
    ### Deletes a comment
    - **isbn**: ISBN of book to get comments
    - **comment_id**: Id of comment to delete
    """
    try:
        if bookStore.deleteComment(isbn, comment_id):
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return getErrorMsg(ERROR_COMMENT_NOT_FOUND)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return getErrorMsg(ERROR_UNKNOWN, str(e))
