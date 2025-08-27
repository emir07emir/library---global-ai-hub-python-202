from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ValidationError
import os
import json
import httpx


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
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}) - {'Available' if self.is_available else 'Not Available'}"


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

    def fetch_book_info(self, isbn: str) -> Optional[Dict[str, Any]]:
        """
        Open Library API'den ISBN ile kitap bilgilerini çeker
        Farklı API endpoint'lerini dener
        """
        # Farklı API endpoint'lerini dene
        api_endpoints = [
            f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data",
            f"https://openlibrary.org/isbn/{isbn}.json",
        ]

        for i, url in enumerate(api_endpoints):
            try:
                print(f"API endpoint {i+1} deneniyor: {url}")
                # User-Agent header'ı ekle
                headers = {"User-Agent": "LibraryApp/1.0 (iemir@example.com)"}

                with httpx.Client(timeout=15.0) as client:
                    response = client.get(url, headers=headers)
                    print(f"API yanıt kodu: {response.status_code}")

                    if response.status_code == 200:
                        data = response.json()
                        print(f"API yanıtı alındı, veri işleniyor...")
                        # ilk endpoint -partner api
                        if i == 0:
                            isbn_key = f"ISBN:{isbn}"
                            if isbn_key in data and data[isbn_key]:
                                book_data = data[isbn_key]
                                result = self._extract_book_info_from_partner_api(
                                    book_data, isbn
                                )
                                if result:
                                    return result
                        # ikinci endpoint - isbn api
                        elif i == 1:
                            if data:
                                result = self._extract_book_info_from_isbn_api(
                                    data, isbn
                                )
                                if result:
                                    return result
                    elif response.status_code == 404:
                        print(f"Endpoint {i+1}: Kitap bulunamadı (404)")
                    else:
                        print(f"Endpoint {i+1}: API hatası {response.status_code}")

            except httpx.RequestError as e:
                print(f"Endpoint {i+1} ağ hatası: {e}")
                continue
            except httpx.TimeoutException:
                print(f"Endpoint {i+1} zaman aşımı")
                continue
            except Exception as e:
                print(f"Endpoint {i+1} beklenmeyen hata: {e}")
                continue

        print(f"Tüm API endpoint'leri denendi ama ISBN {isbn} ile kitap bulunamadı.")
        print("Bu ISBN Open Library veritabanında olmayabilir.")
        return None

    def _extract_book_info_from_partner_api(
        self, book_data: Dict, isbn: str
    ) -> Optional[Dict[str, Any]]:
        """Partner API'den gelen veriyi işler"""
        try:
            title = book_data.get("title", "")
            if not title:
                print("Kitap başlığı bulunamadı")
                return None

            authors = book_data.get("authors", [])
            author_name = "Bilinmeyen Yazar"
            if authors and len(authors) > 0:
                author_name = authors[0].get("name", "Bilinmeyen Yazar")

            publish_date = book_data.get("publish_date", "")
            year = self._extract_year(publish_date)
            result = {"title": title, "author": author_name, "isbn": isbn, "year": year}
            print(f"Partner API'den başarıyla çıkarıldı: {result}")
            return result

        except Exception as e:
            print(f"Partner API veri işleme hatası: {e}")
            return None

    def _extract_book_info_from_isbn_api(
        self, book_data: Dict, isbn: str
    ) -> Optional[Dict[str, Any]]:
        """ISBN API'den gelen veriyi işler"""
        try:
            title = book_data.get("title", "")
            if not title:
                print("Kitap başlığı bulunamadı")
                return None
            authors = book_data.get("authors", [])
            author_name = "Bilinmeyen Yazar"
            if authors and len(authors) > 0:
                author_name = authors[0].get("name", "Bilinmeyen Yazar")
            publish_date = book_data.get("publish_date", "")
            year = self._extract_year(publish_date)
            result = {"title": title, "author": author_name, "isbn": isbn, "year": year}
            print(f"ISBN API'den başarıyla çıkarıldı: {result}")
            return result
        except Exception as e:
            print(f"ISBN API veri işleme hatası: {e}")
            return None

    def _extract_year(self, publish_date: str) -> int:
        """Yayın tarihinden yılı çıkarır"""
        if not publish_date:
            return 2000
        try:
            # Tarih formatını kontrol et
            if "-" in publish_date:
                year_str = publish_date.split("-")[0]
                if year_str.isdigit():
                    return int(year_str)
            elif publish_date.isdigit():
                return int(publish_date)
            import re

            year_match = re.search(r"\b(19|20)\d{2}\b", publish_date)
            if year_match:
                return int(year_match.group())
        except (ValueError, IndexError):
            pass
        return 2000  # varsayılan yıl

    def add_book_by_isbn(self, isbn: str, book_type: str = "1") -> bool:
        """
        ISBN ile kitap ekler
        """
        # Önce ISBN'nin kütüphanede olup olmadığını kontrol et
        for existing_book in self._books:
            if existing_book.ISBN == isbn:
                print(f"ISBN {isbn} ile kitap zaten kütüphanede mevcut.")
                return False

        # Kitap bilgilerini Open Library API'den çek
        book_info = self.fetch_book_info(isbn)
        if not book_info:
            return False
        # Kitap türüne göre yeni kitap nesnesi oluştur
        try:
            if book_type == "1":
                new_book = Book(
                    book_info["title"],
                    book_info["author"],
                    book_info["isbn"],
                    book_info["year"],
                )
            elif book_type == "2":
                format_type = input("Dosya formatı (PDF, EPUB, vb.): ")
                size = float(input("Dosya boyutu (GB): "))
                new_book = Ebook(
                    book_info["title"],
                    book_info["author"],
                    book_info["isbn"],
                    book_info["year"],
                    format_type,
                    size,
                )
            elif book_type == "3":
                duration = float(input("Süre (saat): "))
                new_book = Audiobook(
                    book_info["title"],
                    book_info["author"],
                    book_info["isbn"],
                    book_info["year"],
                    duration,
                )
            elif book_type == "4":
                issue = int(input("Issue numarası: "))
                new_book = Comics(
                    book_info["title"],
                    book_info["author"],
                    book_info["isbn"],
                    book_info["year"],
                    issue,
                )
            else:
                print("Geçersiz kitap türü!")
                return False
            self._books.append(new_book)
            self.save_books()
            print(
                f"Kitap '{new_book.title}' yazar {new_book.author} kütüphaneye eklendi."
            )
            return True
        except ValueError as e:
            print(f"Giriş hatası: {e}")
            return False
        except Exception as e:
            print(f"Kitap ekleme hatası: {e}")
            return False

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
