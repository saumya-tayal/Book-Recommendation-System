import pandas as pd

df = pd.read_csv("books.csv")

# remove spaces in column names
df.columns = df.columns.str.strip()

# convert date
df["publication_date"] = pd.to_datetime(df["publication_date"])

# remove unwanted columns
df = df.drop(
    columns=[
        "isbn",
        "text_reviews_count",
        "publisher"
    ]
)

# keep most popular edition
df = df.sort_values(
    "ratings_count",
    ascending=False
)

df = df.drop_duplicates(
    subset=["title", "authors"],
    keep="first"
)

# optional: sort back by ID
df = df.sort_values("bookID")

# save ACTUAL cleaned data
df.to_csv(
    "cleaned_books.csv",
    index=False
)
print(df.shape)
df = pd.read_csv("cleaned_books.csv")