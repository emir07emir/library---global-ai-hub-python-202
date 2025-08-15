import os
import json


class Book:
    def __init__(self, title, author, ISBN, year, is_available=True):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.year = year
        self.is_available = is_available

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
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}) - {'Available' if self.is_available else 'Not Available'}"


class Ebook(Book):
    def __init__(
        self, title, author, ISBN, year, file_format, file_size, is_available=True
    ):
        super().__init__(title, author, ISBN, year, is_available)
        self.file_format = file_format
        self.file_size = file_size

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}, Format: {self.file_format}, Size: {self.file_size}GB) - {'Available' if self.is_available else 'Not Available'}"


class Audiobook(Book):
    def __init__(self, title, author, ISBN, year, duration, is_available=True):
        super().__init__(title, author, ISBN, year, is_available)
        self.duration = duration

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}, Duration: {self.duration} hours) - {'Available' if self.is_available else 'Not Available'}"


class Comics(Book):
    def __init__(self, title, author, ISBN, year, issue_number, is_available=True):
        super().__init__(title, author, ISBN, year, is_available)
        self.issue_number = issue_number

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}, Issue: {self.issue_number}) - {'Available' if self.is_available else 'Not Available'}"


class Library:
    def __init__(self, name, filename="library.json"):
        self.name = name
        self.filename = filename
        self._books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                books_data = json.load(file)
                self._books = []
                for data in books_data:
                    if "file_format" in data:
                        book = Ebook(**data)
                    elif "duration" in data:
                        book = Audiobook(**data)
                    elif "issue_number" in data:
                        book = Comics(**data)
                    else:
                        book = Book(**data)
                    self._books.append(book)
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

    def add_book(self, book):
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
