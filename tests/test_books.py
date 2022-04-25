from data.openapi import OpenApiStore

# Test getting a book by ISBN
def test_get_book_by_isbn():
    bookStore = OpenApiStore.getInstance()
    book = bookStore.getBookByISBN("9780980200447")    
    print(book)
    assert book, "One and only one book should have been returned"
    assert book.isbn == '9780980200447', "Wrong book return"
    assert book.title == 'Slow reading', "Wrong title"    

    books = bookStore.getBookByISBN("ffff")
    assert not books, "No book should have been returned"

# Test getting a list of books by ISBN
def test_get_books_by_isbn():
    bookStore = OpenApiStore.getInstance()
    books = bookStore.getBooksByISBN("9780980200447,0201558025")    
    assert books and len(books) == 2, "One and only one book should have been returned"
    assert books[0].isbn == '9780980200447', "Wrong book return"
    assert books[0].title == 'Slow reading', "Wrong title"   
    assert books[1].isbn == '0201558025', "Wrong book return"
    assert books[1].title == 'Concrete mathematics', "Wrong title"   

# Test searching books by title
def test_search_by_title():
    bookStore = OpenApiStore.getInstance()
    search_text = "Hobbit"
    books = bookStore.searchByTitle(search_text, limit=10)
    assert books 
    assert len(books) > 0 and len(books) <= 10
    search_text = search_text.lower()
    for book in books:
        assert search_text in book.title.lower(), "Unmatched return"
