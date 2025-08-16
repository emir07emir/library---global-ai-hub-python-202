import pytest
import httpx
from unittest.mock import patch, Mock
from library import Library, Book, Ebook, Audiobook, Comics


class TestLibraryAPI:

    def setup_method(self):
        """Her test öncesi çalışır"""
        self.library = Library("Test Library", "test_library.json")

    def teardown_method(self):
        """Her test sonrası çalışır"""
        # Test dosyasını temizle
        import os

        if os.path.exists("test_library.json"):
            os.remove("test_library.json")

    @patch("httpx.Client")
    def test_fetch_book_info_success(self, mock_client):
        """Başarılı API çağrısı testi"""
        # Mock response oluştur
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ISBN:1234567890": {
                "title": "Test Book",
                "authors": [{"name": "Test Author"}],
                "publish_date": "2020-01-01",
            }
        }

        # Mock client ayarla
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # Test et
        result = self.library.fetch_book_info("1234567890")

        assert result is not None
        assert result["title"] == "Test Book"
        assert result["author"] == "Test Author"
        assert result["isbn"] == "1234567890"
        assert result["year"] == 2020

    @patch("httpx.Client")
    def test_fetch_book_info_not_found(self, mock_client):
        """Kitap bulunamadığında test"""
        # Mock response oluştur
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # Boş response

        # Mock client ayarla
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # Test et
        result = self.library.fetch_book_info("9999999999")

        assert result is None

    @patch("httpx.Client")
    def test_fetch_book_info_network_error(self, mock_client):
        """Ağ hatası durumunda test"""
        # Mock client hata fırlatacak şekilde ayarla
        mock_client_instance = Mock()
        mock_client_instance.get.side_effect = httpx.RequestError("Network error")
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # Test et
        result = self.library.fetch_book_info("1234567890")

        assert result is None

    @patch("httpx.Client")
    def test_fetch_book_info_timeout(self, mock_client):
        """Zaman aşımı durumunda test"""
        # Mock client timeout fırlatacak şekilde ayarla
        mock_client_instance = Mock()
        mock_client_instance.get.side_effect = httpx.TimeoutException("Timeout")
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # Test et
        result = self.library.fetch_book_info("1234567890")

        assert result is None

    @patch("httpx.Client")
    def test_add_book_by_isbn_success(self, mock_client):
        """ISBN ile başarılı kitap ekleme testi"""
        # Mock response oluştur
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "ISBN:1234567890": {
                "title": "Test Book",
                "authors": [{"name": "Test Author"}],
                "publish_date": "2020-01-01",
            }
        }

        # Mock client ayarla
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance

        # Test et
        with patch("builtins.input", side_effect=["1"]):  # Normal kitap seçimi
            result = self.library.add_book_by_isbn("1234567890", "1")

        assert result is True
        assert len(self.library._books) == 1
        assert self.library._books[0].title == "Test Book"

    def test_add_book_by_isbn_duplicate(self):
        """Aynı ISBN ile tekrar ekleme testi"""
        # Önce bir kitap ekle
        book = Book("Test Book", "Test Author", "1234567890", 2020)
        self.library.add_book(book)

        # Aynı ISBN ile tekrar eklemeye çalış
        with patch("library.Library.fetch_book_info") as mock_fetch:
            mock_fetch.return_value = {
                "title": "Another Book",
                "author": "Another Author",
                "isbn": "1234567890",
                "year": 2021,
            }

            result = self.library.add_book_by_isbn("1234567890", "1")

        assert result is False
        assert len(self.library._books) == 1  # Yeni kitap eklenmemeli

    def test_add_book_by_isbn_invalid_type(self):
        """Geçersiz kitap türü ile ekleme testi"""
        with patch("library.Library.fetch_book_info") as mock_fetch:
            mock_fetch.return_value = {
                "title": "Test Book",
                "author": "Test Author",
                "isbn": "1234567890",
                "year": 2020,
            }

            result = self.library.add_book_by_isbn("1234567890", "5")  # Geçersiz tür

        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
