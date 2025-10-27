from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
import os
# import uvicorn

DATA_FILE = "./raw_books/books_with_country.csv"
app = FastAPI(title="Books API", version="1.0")

if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"{DATA_FILE} not found.")
books_df = pd.read_csv(DATA_FILE)

class Book(BaseModel):
    book_title: str
    price: str
    availability: int
    link: str
    rating: int
    publisher_country: str

@app.get("/books")
def get_books(country: str = Query(None)):
    if country:
        filtered = books_df[books_df["publisher_country"].str.lower() == country.lower()]
        return filtered.to_dict(orient="records")
    return books_df.to_dict(orient="records")

@app.post("/books")
def add_book(book: Book):
    global books_df
    if book.book_title in books_df["book_title"].values:
        raise HTTPException(400, "Book already exists.")
    books_df = pd.concat([books_df, pd.DataFrame([book.dict()])], ignore_index=True)
    books_df.to_csv(DATA_FILE, index=False, encoding="utf-8")
    return {"message": "Book added.", "book": book}

@app.delete("/books/{title}")
def delete_book(title: str):
    global books_df
    if title not in books_df["book_title"].values:
        raise HTTPException(404, "Book not found.")
    books_df = books_df[books_df["book_title"] != title]
    books_df.to_csv(DATA_FILE, index=False, encoding="utf-8")
    return {"message": f"Book '{title}' deleted."}

# if __name__ == '__main__':
#     uvicorn.run(app='p3_books_api:app')


