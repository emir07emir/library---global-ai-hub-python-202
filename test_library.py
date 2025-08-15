import pytest
import os
from book import Book
from library import Library

# -------------------------
# Fixture: temiz Library
# -------------------------
@pytest.fixture
def library():
    # Test için geçici JSON dosyası
    test_file = "test_library.json"
    # Dosya varsa sil
    if os.path.exists(test_file):
        os.remove(test_file)
    lib = Library(filename=test_file)
    return lib

# -------------------------
# Book sınıfı testleri
# -------------------------
def test_book_creation():
    book = Book("The Hobbit", "J.R.R. Tolkien", "978-3-16-148410-0", 1937)
    assert book.title == "The Hobbit"
    assert book.author == "J.R.R. Tolkien"
    assert book.ISBN == "978-3-16-148410-0"
    assert book.year == 1937
    assert book.is_available is True

def test_borrow_and_return():
    book = Book("Dune", "Frank Herbert", "978-0-441-17271-9", 1965)
    book.borrow_book()
    assert book.is_available is False
    book.return_book()
    assert book.is_available is True

# -------------------------
# Library sınıfı testleri
# -------------------------
def test_add_book(library):
    book = Book("1984", "George Orwell", "12345", 1949)
    library.add_book(book)
    assert len(library._books) == 1
    assert library._books[0].title == "1984"

def test_remove_book(library):
    book = Book("1984", "George Orwell", "12345", 1949)
    library.add_book(book)
    result = library.remove_book("12345")
    assert result is True
    assert len(library._books) == 0

def test_remove_book_not_found(library):
    result = library.remove_book("00000")
    assert result is False

def test_find_book(library):
    book = Book("1984", "George Orwell", "12345", 1949)
    library.add_book(book)
    found = library.find_book("12345")
    assert found.title == "1984"

def test_list_books(library):
    book1 = Book("1984", "George Orwell", "12345", 1949)
    book2 = Book("Sefiller", "Victor Hugo", "67890", 1862)
    library.add_book(book1)
    library.add_book(book2)
    books = library.list_books()
    assert len(books) == 2
    assert books[1].title == "Sefiller"

def test_save_and_load_books(library):
    book = Book("1984", "George Orwell", "12345", 1949)
    library.add_book(book)
    # JSON dosyasına kaydet
    library.save_books()

    # Yeni bir Library instance ile yükle
    new_lib = Library(filename="test_library.json")
    assert len(new_lib._books) == 1
    assert new_lib._books[0].title == "1984"

