from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import book as book_model
from app.schemas import book as book_schema
from app.services import GroqService
from app.services.gutenberg import GutenbergService
from app.services.text_analysis import TextAnalysisService
from typing import List
import logging

router = APIRouter(prefix="/books", tags=["books"])
text_analysis_service = TextAnalysisService()
groq_service = GroqService()


@router.post("/", response_model=book_schema.Book)
async def create_book(book: book_schema.BookCreate, db: Session = Depends(get_db)):
    try:
        # Check if book already exists
        existing_book = db.query(book_model.Book).filter(
            book_model.Book.gutenberg_id == book.gutenberg_id
        ).first()

        if existing_book:
            return existing_book

        # Get book from Gutenberg
        book_data = GutenbergService.get_book(book.gutenberg_id)

        # Create book in database
        db_book = book_model.Book(
            gutenberg_id=book.gutenberg_id,
            title=book_data["metadata"]["title"],
            author=book_data["metadata"]["author"],
            content=book_data["content"],
            book_metadata=book_data["metadata"]
        )

        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    except Exception as e:
        logging.error(f"Error creating book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error fetching or creating book: {str(e)}"
        )


@router.get("/", response_model=List[book_schema.Book])
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(book_model.Book).offset(skip).limit(limit).all()
    return books


@router.get("/{book_id}", response_model=book_schema.Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(book_model.Book).filter(book_model.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/{book_id}/analysis", response_model=book_schema.TextAnalysisGroq)
async def analyze_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(book_model.Book).filter(book_model.Book.id == int(book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    analysis = groq_service.analyze_book(book.content)

    data = {
        "gutenberg_id": book.gutenberg_id,
        "title": book.title,
    }

    return {**data, **analysis}
