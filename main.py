from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database, init_db

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db.init_db(database.SessionLocal())

@app.post("/authors/")
def create_author(author: models.Author, db: Session = Depends(get_db)):
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

@app.post("/books/")
def create_book(book: models.Books, db: Session = Depends(get_db)):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.post("/reviews/")
def create_review(review: models.Review, db: Session = Depends(get_db)):
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

