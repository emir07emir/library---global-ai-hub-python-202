// API base URL
const API_BASE = 'http://127.0.0.1:8001';

// DOM elementleri
const addBookForm = document.getElementById('addBookForm');
const booksList = document.getElementById('booksList');
const loading = document.getElementById('loading');
let mesajkutusu = document.querySelector(".mesajkutusu");

// Sayfa yüklendiğinde kitapları getir
document.addEventListener('DOMContentLoaded', function() {
    loadBooks();
});

// Form submit event
addBookForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const isbn = document.getElementById('isbn').value.trim();
    if (isbn) {
        addBook(isbn);
    }
});

// Kitapları yükle
async function loadBooks() {
    try {
        loading.style.display = 'block';
        booksList.style.display = 'none';
        
        const response = await fetch(`${API_BASE}/books`);
        if (response.ok) {
            const books = await response.json();
            displayBooks(books);
        } else {
            console.error('Kitaplar yüklenemedi:', response.status);
        }
    } catch (error) {
        console.error('Hata:', error);
    } finally {
        loading.style.display = 'none';
        booksList.style.display = 'grid';
    }
}

// Kitap ekle
async function addBook(isbn) {
    try {
        // ISBN harf kontrolü (önce harf var mı kontrol et)
        if (!/^\d+$/.test(isbn)) {
            mesaj("danger","ISBN numarası harf içeremez!");
            addBookForm.reset();
            
            return;
        }
        
        // ISBN uzunluk kontrolü
        if (isbn.length !== 13) {
            mesaj("warning","ISBN numarası 13 haneli olmalıdır!");
            addBookForm.reset();
            return;   
        }
        
        const response = await fetch(`${API_BASE}/books`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ isbn: isbn })
        });
        
        if (response.ok) {
            const book = await response.json();
            console.log('Kitap eklendi:', book);
            mesaj("success","Kitap başarıyla eklendi.")
            addBookForm.reset();
            loadBooks(); // Listeyi yenile
        } else {
            const error = await response.json();
            console.error('Kitap eklenemedi:', error.detail);
            mesaj("danger",`${error.detail}`);
            addBookForm.reset();
        }
    } catch (error) {
        console.error('Hata:', error);
        alert('Kitap eklenirken hata oluştu');
    }
}

// Kitap sil
async function deleteBook(isbn) {
    if (confirm('Bu kitabı silmek istediğinizden emin misiniz?')) {
        try {
            const response = await fetch(`${API_BASE}/books/${isbn}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                console.log('Kitap silindi');
                mesaj("success",`${isbn} ISBN numaralı kitap silindi`)
                loadBooks(); // Listeyi yenile
            } else {
                console.error('Kitap silinemedi:', response.status);
            }
        } catch (error) {
            console.error('Hata:', error);
        }
    }
}

// Kitapları görüntüle
function displayBooks(books) {
    if (books.length === 0) {
        booksList.innerHTML = '<p>Henüz kitap eklenmemiş.</p>';
        return;
    }
    
    const booksHTML = books.map(book => `
        <div class="book-item">
            <h3>${book.title}</h3>
            <p><strong>Yazar:</strong> ${book.author}</p>
            <p><strong>ISBN:</strong> ${book.isbn}</p>
            <p><strong>Yıl:</strong> ${book.year}</p>
            <p><strong>Durum:</strong> ${book.is_available ? 'Mevcut' : 'Ödünç'}</p>
            <button onclick="deleteBook('${book.isbn}')" class="delete-btn">Sil</button>
        </div>
    `).join('');
    
    booksList.innerHTML = booksHTML;

}


function mesaj(type, message) {
    //     <div class="alert alert-primary" role="alert">
    //   A simple primary alert—check it out!
    // </div>

    const alert = document.createElement("div");
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    mesajkutusu.appendChild(alert);
    

    setTimeout(function () {
        alert.remove();
    }, 2500)


}