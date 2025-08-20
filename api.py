from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from library import Library, Book, Ebook, Audiobook, Comics


class BookModel(BaseModel):
    title: str
    author: str
    isbn: str
    year: int
    is_available: bool = True
    # İlgili kitap türleri için opsiyonel alanlar
    file_format: Optional[str] = None
    file_size: Optional[float] = None
    duration: Optional[float] = None
    issue_number: Optional[int] = None


class ISBNRequest(BaseModel):
    isbn: str


app = FastAPI(title="Library API", version="1.0.0")

# Uygulama seviyesinde tek bir Library örneği
library = Library("City Library")


def _book_to_model(book: Book) -> BookModel:
    base = {
        "title": book.title,
        "author": book.author,
        "isbn": book.ISBN,
        "year": book.year,
        "is_available": getattr(book, "is_available", True),
    }
    # Tür bazlı alanlar
    if isinstance(book, Ebook):
        base.update({
            "file_format": getattr(book, "file_format", None),
            "file_size": getattr(book, "file_size", None),
        })
    elif isinstance(book, Audiobook):
        base.update({
            "duration": getattr(book, "duration", None),
        })
    elif isinstance(book, Comics):
        base.update({
            "issue_number": getattr(book, "issue_number", None),
        })
    return BookModel(**base)


@app.get("/books", response_model=List[BookModel])
def get_books():
    return [_book_to_model(b) for b in getattr(library, "_books", [])]


@app.post("/books", response_model=BookModel, status_code=status.HTTP_201_CREATED)
def add_book(isbn_req: ISBNRequest):
    isbn = isbn_req.isbn.strip()
    if not isbn:
        raise HTTPException(status_code=400, detail="ISBN boş olamaz")

    # Mevcutta var mı?
    if library.find_book(isbn):
        raise HTTPException(status_code=409, detail=f"ISBN {isbn} zaten mevcut")

    success = library.add_book_by_isbn(isbn, book_type="1")
    if not success:
        # Başarısızsa ve hâlâ yoksa Open Library'den bulunamadı varsayalım
        if not library.find_book(isbn):
            raise HTTPException(status_code=404, detail=f"ISBN {isbn} için kitap bulunamadı")

    added = library.find_book(isbn)
    if not added:
        # Her ihtimale karşı
        raise HTTPException(status_code=500, detail="Kitap eklenemedi")
    return _book_to_model(added)


@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    existing = library.find_book(isbn)
    if not existing:
        raise HTTPException(status_code=404, detail=f"ISBN {isbn} bulunamadı")
    library.remove_book(isbn)
    return {"detail": f"ISBN {isbn} silindi"}


