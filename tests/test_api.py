import requests
import sqlite3
from data.dbbookstore import DBBookStore

def test_get_book():
    response = requests.get("http://localhost:8000/book/9780980200447")
    book = response.json()
    assert book['isbn'] == '9780980200447', "Wrong book return"
    assert book['title'] == 'Slow reading', "Wrong title" 

def test_get_invalid_book():
    response = requests.get("http://localhost:8000/book/ffff")
    assert response.status_code == 404

def test_write_book():
    authors = ['Peter Parker', 'Bruce Wayne', 'Bilbo Baggins']
    book_to_save = {'isbn': '9780980200447',
        'title': 'Fast reading',
        'number_of_pages': 100,
        'authors': [{'name': author} for author in authors]
    }
    assert len(book_to_save['authors']) == len(authors)
    response = requests.put("http://localhost:8000/book",
                           json=book_to_save)
    assert response.status_code >= 200 and response.status_code < 300

    # Get the book back
    response = requests.get("http://localhost:8000/book/9780980200447")
    book = response.json()
    assert book['isbn'] == '9780980200447', "Wrong book return"
    assert book['title'] == 'Fast reading', "Wrong title" 
    assert len(book['authors']) == len(authors), "Wrong number of authors added"
    for author in book['authors']:
        assert author['name'] in authors, "Wrong author added"
    book_authors = [author['name'] for author in book['authors']]
    for author in authors:
        assert author in book_authors, "Author not added"
    # Remove the book from db again 
    dbbook = DBBookStore.getInstance()
    dbbook.removeBookByISBN('9780980200447')
    for author in authors:
        dbbook.removeAuthor(author)

def test_add_comment_missing_book():
    response = requests.put("http://localhost:8000/book/ffff/comment",
                           json={
                               'user_name': 'Nobody',
                               'subject': 'No added',
                               'text': 'This comment wont be added'
                           })
    assert response.status_code == 404

def test_comments():
    comments = [
        {
        'user_name': 'Peter Parker',
        'subject': 'Great book!',
        'text': 'This is a great book. You should read it'
        },
        {
        'user_name': 'Bilbo Baggins',
        'subject': 'Good book!',
        'text': 'This is a good book. You should read it'
        },
        {
        'user_name': 'Bruce Wayne',
        'subject': 'Not such a good book!',
        'text': 'This is a bad book. You should not read it'
        },
    ]
    response = requests.get("http://localhost:8000/book/9780980200447/comments")
    assert response.status_code == 200
    prev_comments = response.json()
    for comment in comments:
        response = requests.put("http://localhost:8000/book/9780980200447/comment",
                                json=comment)
        assert response.status_code >= 200 and response.status_code < 300
    response = requests.get("http://localhost:8000/book/9780980200447/comments")
    assert response.status_code == 200
    new_comments = response.json()
    assert len(new_comments) == len(prev_comments) + len(comments)
    fields = ['user_name', 'subject', 'text']
    comments_added = []
    for comment in comments:
        found = False
        for new_comment in new_comments:
            found = all(new_comment[field] == comment[field] for field in fields)
            if found:
                comments_added.append(new_comment)
                break
        assert found, "Some comment was not added"

    # Test modifying
    for comment in comments_added:
        upd_comment = comment.copy()
        for field in fields:
            upd_comment[field] = upd_comment[field] + " changed"
        response = requests.post("http://localhost:8000/book/9780980200447/comment",
                                 json=upd_comment)
        assert response.status_code == 200

    response = requests.get("http://localhost:8000/book/9780980200447/comments")
    assert response.status_code == 200
    new_comments = response.json()
    for comment in comments_added:
        found = False
        for new_comment in new_comments:
            found = new_comment['comment_id'] == comment['comment_id']
            if found:
                changed = all(new_comment[field] == comment[field] + " changed" for field in fields)
                assert changed, "Comment was not successfully changed %s - %s" % (new_comment, comment) 
                break
        assert found, "Error updating comment"

    for comment in comments_added:
        response = requests.delete("http://localhost:8000/book/9780980200447/comment/%s" % comment['comment_id'])
        assert response.status_code == 200
    response = requests.get("http://localhost:8000/book/9780980200447/comments")
    assert response.status_code == 200
    new_comments = response.json()
    assert len(prev_comments) == len(new_comments), "Some comments were not deleted"

    # Check deleting the same comments again
    for comment in comments_added:
        response = requests.delete("http://localhost:8000/book/9780980200447/comment/%s" % comment['comment_id'])
        assert response.status_code == 404
            

def test_search():
    # Test the search of books
    # We will just test that all books title containe the search text
    response = requests.get("http://localhost:8000/search_books?title=hobbit&limit=10")
    results = response.json()
    assert len(results) <= 10, "Too many books return"
    assert len(results) > 0, "There should be at least one book with title containing the word hobbit"
    for book in results:
        assert "hobbit" in book['title'].lower(), "Found one book not containing the search word"

def test_save_invalid_book():
    authors = ['Peter Parker', 'Bruce Wayne', 'Bilbo Baggins']
    book_to_save = {'isbn': '9780980200447',
        'title': 'F',  # Title too short
        'number_of_pages': 100,
        'authors': [{'name': author} for author in authors]
    }
    response = requests.put("http://localhost:8000/book",
                           json=book_to_save)
    assert response.status_code >= 400

def test_save_invalid_comment():
    comment = {
        'user_name': 'P', # User name too short
        'subject': 'Great book!',
        'text': 'This is a great book. You should read it'
    }
    response = requests.put("http://localhost:8000/book/9780980200447/comment",
                            json=comment)
    assert response.status_code >= 400