# library.py dosyasından gerekli sınıfları import ediyoruz
from library import Library, Book, Ebook, Audiobook, Comics

def main():
    # Önce bir kütüphane nesnesi oluşturuyoruz
    my_library = Library("Benim Kütüphanem")
    
    print("=== KÜTÜPHANE YÖNETİM SİSTEMİ ===")
    
    while True:
        print("\nMenü:")
        print("1. Kitap Ekle")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış Yap")
        
        secim = input("\nSeçiminizi yapın (1-5): ")
        
        if secim == "1":
            # Kitap ekleme
            print("\n--- KİTAP EKLEME ---")
            print("Kitap türü seçin:")
            print("1. Normal Kitap")
            print("2. E-Kitap")
            print("3. Sesli Kitap")
            print("4. Çizgi Roman")
            
            book_type = input("Seçiminiz (1-4): ")
            
            title = input("Kitap başlığı: ")
            author = input("Yazar: ")
            isbn = input("ISBN: ")
            year = int(input("Yayın yılı: "))
            
            if book_type == "1":
                # Normal kitap oluştur
                new_book = Book(title, author, isbn, year)
            elif book_type == "2":
                # E-kitap oluştur
                format_type = input("Dosya formatı (PDF, EPUB, vb.): ")
                size = float(input("Dosya boyutu (GB): "))
                new_book = Ebook(title, author, isbn, year, format_type, size)
            elif book_type == "3":
                # Sesli kitap oluştur
                duration = float(input("Süre (saat): "))
                new_book = Audiobook(title, author, isbn, year, duration)
            elif book_type == "4":
                # Çizgi roman oluştur
                issue = int(input("Sayı numarası: "))
                new_book = Comics(title, author, isbn, year, issue)
            else:
                print("Geçersiz seçim!")
                continue
            
            # Kitabı kütüphaneye ekle
            my_library.add_book(new_book)
            
        elif secim == "2":
            # Kitap silme
            print("\n--- KİTAP SİLME ---")
            isbn = input("Silinecek kitabın ISBN'ini girin: ")
            my_library.remove_book(isbn)
            
        elif secim == "3":
            # Kitapları listeleme
            print("\n--- KİTAP LİSTESİ ---")
            my_library.list_books()
            print(f"\nToplam kitap sayısı: {my_library.total_books()}")
            
        elif secim == "4":
            # Kitap arama
            print("\n--- KİTAP ARAMA ---")
            isbn = input("Aranacak kitabın ISBN'ini girin: ")
            found_book = my_library.find_book(isbn)
            if found_book:
                print(f"Kitap bulundu: {found_book}")
            else:
                print("Kitap bulunamadı.")
                
        elif secim == "5":
            print("Program sonlandırılıyor...")
            print("Çıkış Yapıldı")
            break
            
        else:
            print("Geçersiz seçim! Lütfen 1-5 arasında bir sayı girin.")

if __name__ == "__main__":
    main()









