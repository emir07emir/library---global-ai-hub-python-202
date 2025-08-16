from dataclasses import dataclass, field
from typing import List, Optional, Union
from pydantic import BaseModel, ValidationError
import os
import json


@dataclass
class Book:
    title: str
    author: str
    ISBN: str
    year: int
    is_available: bool = True

    def borrow_book(self):
        if self.is_available:
            self.is_available = False
            return f"You have borrowed '{self.title}' by {self.author}."
        else:
            print(f"'{self.title}' is currently borrowed.")

    def return_book(self):
        if not self.is_available:
            self.is_available = True
            return f"You have returned '{self.title}' by {self.author}."
        else:
            print(f"'{self.title}' was not borrowed.")

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}) - 'Available' if {self.is_available} else 'Not Available'"


@dataclass
class Ebook(Book):
    file_format: str = ""
    file_size: float = 0.0

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}, Format: {self.file_format}, Size: {self.file_size}GB) - {'Available' if self.is_available else 'Not Available'}"


@dataclass
class Audiobook(Book):
    duration: float = 0.0

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}, Duration: {self.duration} hours) - {'Available' if self.is_available else 'Not Available'}"


@dataclass
class Comics(Book):
    issue_number: int = 0

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}, Issue: {self.issue_number}) - {'Available' if self.is_available else 'Not Available'}"


# Pydantic models
class BookModel(BaseModel):
    title: str
    author: str
    ISBN: str
    year: int
    is_available: bool = True
    file_format: Optional[str] = None
    file_size: Optional[float] = None
    duration: Optional[float] = None
    issue_number: Optional[int] = None


class Library:
    def __init__(self, name, filename="library.json"):
        self.name = name
        self.filename = filename
        self._books: List[Book] = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                books_data = json.load(file)
                self._books = []
                for data in books_data:
                    try:
                        validated = BookModel(**data)
                        if validated.file_format is not None:
                            book = Ebook(
                                validated.title,
                                validated.author,
                                validated.ISBN,
                                validated.year,
                                validated.file_format,
                                validated.file_size or 0.0,
                                validated.is_available,
                            )
                        elif validated.duration is not None:
                            book = Audiobook(
                                validated.title,
                                validated.author,
                                validated.ISBN,
                                validated.year,
                                validated.duration,
                                validated.is_available,
                            )
                        elif validated.issue_number is not None:
                            book = Comics(
                                validated.title,
                                validated.author,
                                validated.ISBN,
                                validated.year,
                                validated.issue_number,
                                validated.is_available,
                            )
                        else:
                            book = Book(
                                validated.title,
                                validated.author,
                                validated.ISBN,
                                validated.year,
                                validated.is_available,
                            )
                        self._books.append(book)
                    except ValidationError as e:
                        print(f"Validation error: {e}")
        else:
            self._books = []

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(
                [book.__dict__ for book in self._books],
                file,
                indent=4,
                ensure_ascii=False,
            )

    def add_book(self, book: Book):
        if not isinstance(book, Book):
            raise TypeError("Only instances of Book or its subclasses can be added.")
        for existing_book in self._books:
            if existing_book.ISBN == book.ISBN:
                print(f"Book with ISBN {book.ISBN} already exists in the library.")
                return
        self._books.append(book)
        self.save_books()
        print(f"Book {book.title} has been added to library {self.name}.")

    def remove_book(self, isbn):
        for book in self._books:
            if book.ISBN == isbn:
                self._books.remove(book)
                self.save_books()
                print(f"Book {book.title} has been removed from library {self.name}.")
                return
        print(f"No book with ISBN {isbn} found in library {self.name}.")

    def list_books(self):
        if not self._books:
            print("No books available in the library.")
        else:
            for book in self._books:
                print(book.__str__())

    def find_book(self, isbn):
        for book in self._books:
            if book.ISBN == isbn:
                return book
        print(f"No book with ISBN {isbn} found in library {self.name}.")

    def total_books(self):
        return len(self._books)


print(mylibrary := Library("My Library"))
print(mylibrary.total_books())
