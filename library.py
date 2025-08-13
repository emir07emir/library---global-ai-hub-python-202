from dataclasses import dataclass, field
from typing import List
from pydantic import BaseModel, Field, ValidationError
from typing import Optional



class Library:
    
    def __init__(self,name:str):
        self.name=name
        self._books = []
        
        
    def add_book(self,book:Book):
        self._books.append(book)
        
    def find_book(self,title:str) -> Optional[Book]:
        for book in self._books:
            if book.title.lower() == title.lower():
                return book #ben buraya a yazsam da olurdu book diyerek tanımladık
            else:
                return None
    
    @property
    def total_books(self)->int:
        return len(self._books)            
        
my_library = Library(name="City Center Library")
my_library.add_book(ebook)
my_library.add_book(audio_book)                

print(my_library.name,"kütüphanesindeki toplam kitap sayısı: ",my_library.total_books)        
found_book = my_library.find_book("1984")      
if found_book:
    print("Bulunan Kitap: ",found_book.title,"by" ,found_book.author)       
else:
    print("Kitap bulunamadı!")        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        