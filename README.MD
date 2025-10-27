# 📚 Books Web Scraping & REST API Project

## 🧩 Project Overview
1. **Part 1:** Scrape book data from https://books.toscrape.com  
2. **Part 2:** Use the REST Countries API to assign random publisher countries  
3. **Part 3:** Build a FastAPI REST API to view, add, and delete books  

---

## ⚙️ Requirements
```powershell
pip install -r requirements.txt
bash setup.sh
```

---

## 🚀 Run Instructions

### 🕷️ 1. Scrape book data
```powershell
python p1_scrape_books.py
```
Output:
- `raw_books/` folder
- `html_backup/` folder

### 🌍 2. Add random countries
```powershell
python p2_add_country_data.py
```
Output:
- `raw_books/books_with_country.csv`
- `raw_books/books_with_country.json`

### 🧠 3. Start REST API
```powershell
uvicorn p3_books_api:app --reload
```
Then open your browser at:

- Docs UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- All books: [http://127.0.0.1:8000/books](http://127.0.0.1:8000/books)

### 💾 Example Requests

#### Filter by country: 
```powershell
curl.exe -X GET http://127.0.0.1:8000/books?country=Slovakia
```
#### How to add a new book:
Create a file `book_add.json`:
```commandline  
{
        "book_title": "Test Book",
        "price": "£12.99",
        "availability": 16,
        "link": "https://example.com",
        "rating": 5,
        "publisher_country": "Japan"
}
```
```powershell
curl.exe -X POST "http://127.0.0.1:8000/books" `
-H "Content-Type: application/json" `
-d "@book_add.json"
```
#### Delete a book:
```powershell
curl.exe -X DELETE 'http://127.0.0.1:8000/books/Test%20Book' `
-H 'accept: application/json'
```

## 📂 Output Files
- `raw_books/Self Help_3_books.csv`
- `raw_books/books_with_country.csv`
- `raw_books/books_with_country.json`
- `html_backup/` (raw HTML for each book)

## ⚠️ Notes
- Make sure to run **Part 1** before **Part 2**, and **Part 3** before starting the API.  
- All commands are tested and run in **PowerShell inside PyCharm** for correct execution on Windows.  
- Use PowerShell when executing the `curl.exe` commands to handle special characters properly.
