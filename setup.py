import sqlite3

con = sqlite3.connect('db/books.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS books
               (id integer  PRIMARY KEY  AUTOINCREMENT, isbn text, title text, url text, number_of_pages integer)''')
cur.execute('''CREATE INDEX IF NOT EXISTS book_isbn ON books (isbn)''')

cur.execute('''CREATE TABLE IF NOT EXISTS authors
               (id integer  PRIMARY KEY  AUTOINCREMENT, name text, url text)''')
cur.execute('''CREATE INDEX IF NOT EXISTS author_name ON authors (name)''')

cur.execute('''CREATE TABLE IF NOT EXISTS books_authors
               (author_id integer, book_id integer, PRIMARY KEY(author_id, book_id),
                FOREIGN KEY(author_id) REFERENCES authors(id),
                FOREIGN KEY(book_id) REFERENCES books(id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS comments
               (id integer  PRIMARY KEY  AUTOINCREMENT, 
                user_name text,
                subject text,
                comment text,
                book_isbn text
               )''')
        