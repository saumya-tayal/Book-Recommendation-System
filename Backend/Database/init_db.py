import sqlite3
import pandas as pd


conn = sqlite3.connect("database.db")

cursor = conn.cursor()


# Create books table

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(

    bookID INTEGER PRIMARY KEY,
    title TEXT,
    authors TEXT,
    average_rating REAL,
    isbn13 TEXT,
    language_code TEXT,
    num_pages INTEGER,
    ratings_count INTEGER,
    publication_date TEXT

)
""")


# Create user tracker table

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_books(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    book_id INTEGER,

    status TEXT,

    user_rating INTEGER,

    review TEXT,

    date_added TEXT,

    date_finished TEXT,

    FOREIGN KEY(book_id)
        REFERENCES books(bookID)

)
""")


# load csv

df = pd.read_csv("../Data/cleaned_books.csv")


df.to_sql(
    "books",
    conn,
    if_exists="replace",
    index=False
)


conn.commit()

conn.close()


print("Database created successfully 📚")