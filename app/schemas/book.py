from pydantic import BaseModel
from typing import Optional, Dict

class BookBase(BaseModel):
    gutenberg_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    title: str
    author: str
    book_metadata: Dict  # Changed from 'metadata' to 'book_metadata'
    content: str  # Changed from 'metadata' to 'book_metadata'

    class Config:
        orm_mode = True

class TextAnalysis(BaseModel):
    language: str
    sentiment: float
    key_characters: list[str]
    summary: str
    title: str
    gutenberg_id: int

class TextAnalysisGroq(BaseModel):
    characters: list[str]
    sentiment: list[str]
    language: str
    plot_summary: list[str]
    title: str
    gutenberg_id: int
