from typing import List, Optional
from pydantic import BaseModel, Field

class Author(BaseModel):
    name: str = Field(None, title="Name of author")
    url: Optional[str] = Field(None, title="Url to view page of author")

class Comment(BaseModel):
    comment_id: Optional[int] = Field(None, title="Unique identifier for the comment")
    user_name: str = Field(None, title="Name of user who posted the comment")
    subject: str = Field(None, title="Comment subject")
    text: str = Field(None, title="Comment")

class Book(BaseModel):
    title: str = Field(None, title="Book comment")
    isbn: str = Field(None, title="Book ISBN")
    number_of_pages: int = Field(None, title="Number of pages")
    url: Optional[str] = Field(None, title="URL to view full info about the book")
    authors: List[Author] = Field([], title="List of authors")
    # comments: List[Comment] = Field([], title="List of comments about the book")

class SearchResult(BaseModel):
    title: str
    isbns: List[str] = []
