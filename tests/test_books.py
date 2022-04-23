from data.openapi import OpenApiStore

def test_get_book_by_isbn():
    bookStore = OpenApiStore.getInstance()
    books = bookStore.getBookByISBN("9780980200447")    
    assert books and len(books) == 1, "One and only one book should have been returned"
    assert books[0]['ISBN'] == '9780980200447', "Wrong book return"
    assert books[0]['title'] == 'Slow reading', "Wrong title"    

    books = bookStore.getBookByISBN("ffff")
    assert not books, "No book should have been returned"
