# library---global-ai-hub-python-202
Global AI Hub 'ın gerçekleştirdiği Python202 Bootcamp'i sonucunda oluşturduğum library

# 13.08.2025 16.57 saatinde değişiklik yaptım ve kaydettim
#20.08.2025  23.47
# Library Project - Global AI Hub Python 202

Bu proje, Global AI Hub Python 202 Bootcamp kapsamında geliştirilmiş bir kütüphane uygulamasıdır.  
Üç aşamadan oluşur ve her aşamada proje bir öncekinin üzerine inşa edilmiştir:  

1. Aşama 1 (OOP - Terminal Uygulaması) → Python ile OOP kullanılarak kitap yönetim sistemi.  
2. Aşama 2 (API Entegrasyonu) → OpenLibrary API ile ISBN üzerinden kitap bilgisi çekme.  
3. Aşama 3 (FastAPI + Web Arayüzü) → FastAPI tabanlı REST API ve HTML/CSS/JavaScript ile görsel arayüz.  

GitHub Repo: [library---global-ai-hub-python-202](https://github.com/semanurcoskun/library---global-ai-hub-python-202)

---

## Genel Bakış

Bu proje ile:
- Kitap ekleme, silme, listeleme ve arama işlemleri yapılabilir.
- Harici API kullanılarak ISBN üzerinden kitap bilgileri otomatik çekilebilir.
- FastAPI ile REST API geliştirilmiş ve bu API’yi kullanan HTML/CSS/JS tabanlı web arayüzü eklenmiştir.  

---
## Repo klonlama
git clone https://github.com/semanurcoskun/library---global-ai-hub-python-202.git
cd library---global-ai-hub-python-202

## set up requirements
pip install -r requirements.txt
requirements:
fastapi==0.111.0
uvicorn==0.30.1
httpx==0.27.0
pytest==8.3.1
anyio>=4.0.0

## Kurulum

1. Reponunuzu klonlayın:
   ```bash
   git clone https://github.com/semanurcoskun/library---global-ai-hub-python-202.git
   cd library---global-ai-hub-python-202
   ```

2. Gerekli kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt
   ```

---

## Kullanım

### Aşama 1 - Terminal Uygulaması
```bash
python main.py
```
Menü üzerinden kitap ekleyebilir, silebilir, listeleyebilir veya arayabilirsiniz.  
Veriler library.json dosyasında saklanır.

---

### Aşama 2 - OpenLibrary API Entegrasyonu
Bu aşamada yalnızca ISBN numarası girilerek kitap ekleme özelliği eklenmiştir.
Uygulama OpenLibrary API’sinden kitabın başlık ve yazar bilgilerini otomatik çeker.

---

### Aşama 3 - FastAPI + Web Arayüzü

#### API Sunucusunu Başlatma
```bash
uvicorn api:app --reload
```
#### Sanal ortam oluşturma
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

API Dokümantasyonu: http://127.0.0.1:8000/docs

Endpointler:
- GET /books → Kayıtlı tüm kitapları döndürür.
- POST /books → ISBN ile yeni kitap ekler. (Örnek body: {"isbn": "9780140328721"})
- DELETE /books/{isbn} → ISBN’e göre kitap siler.

#### Web Arayüzü
index.html dosyasını tarayıcıda açarak kitapları listeleyen, yeni kitap ekleyen ve silen basit bir HTML/CSS/JS arayüzü üzerinden API’ye bağlanabilirsiniz.  
Bu sayede terminal kullanmadan görsel olarak kitap yönetimi yapılabilir.

---

## Testler
Tüm aşamalar için pytest testleri yazılmıştır.  
Çalıştırmak için:
```bash
pytest
```

---


## Katkı
Proje Semanur Coşkun ve İbrahim Emir Erdoğan tarafından geliştirilmiştir.
