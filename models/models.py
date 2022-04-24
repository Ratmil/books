from typing import List, Optional
from pydantic import BaseModel

class Author(BaseModel):
    name: str
    url: Optional[str]

class Comment(BaseModel):
    comment_id: Optional[int]
    user_name: str
    subject: str
    text: str

class Book(BaseModel):
    title: str
    isbn: str
    number_of_pages: int
    url: Optional[str]
    authors: List[Author] = []
    comments: List[Comment] = []

class SearchResult(BaseModel):
    title: str
    isbns: List[str] = []
