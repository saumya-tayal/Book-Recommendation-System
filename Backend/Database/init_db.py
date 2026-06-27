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

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password_hash TEXT NOT NULL

)
""")


# Create user tracker table

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_books(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    book_id INTEGER NOT NULL,

    status TEXT,

    user_rating INTEGER,

    review TEXT,

    date_added TEXT,

    date_finished TEXT,

    FOREIGN KEY(user_id)
        REFERENCES users(id),

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



print("Database created successfully 📚")

cursor.execute(
    "SELECT id, name, email FROM users"
)

print(cursor.fetchall())
conn.close()