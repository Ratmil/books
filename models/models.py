from typing import List, Optional
from pydantic import BaseModel

class Author(BaseModel):
    name: str
    url: Optional[str]

class Book(BaseModel):
    title: str
    isbn: str
    number_of_pages: int
    url: Optional[str]
    authors: List[Author] = []

class SearchResult(BaseModel):
    title: str
    isbns: List[str] = []
