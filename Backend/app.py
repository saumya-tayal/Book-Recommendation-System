# Backend code to serve the cleaned data
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

df = pd.read_csv("Data/cleaned_books.csv")


@app.route("/")
def home():
    return "BookNest backend is running!"


@app.route("/books")
def get_books():

    books = df.sort_values(
    "average_rating",
    ascending=False).head(50)

    return jsonify(
        books.to_dict(orient="records")
    )

@app.route("/search")
def search_books():

    query = request.args.get("q", "")

    results = df[
        df["title"]
        .str.contains(
            query,
            case=False,
            na=False
        )
    ]

    return jsonify(
        results.head(50).to_dict(orient="records")
    )


if __name__ == "__main__":
    app.run(debug=True)