from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

def get_db_connection():

    conn = sqlite3.connect(
        "Database/database.db"
    )

    conn.row_factory = sqlite3.Row

    return conn

@app.route("/")
def home():
    return "BookNest backend is running!"


@app.route("/books")
def get_books():

    conn = get_db_connection()

    books = conn.execute(
        "SELECT * FROM books LIMIT 50"
    ).fetchall()

    conn.close()


    return jsonify(
        [dict(book) for book in books]
    )

@app.route("/signup", methods=["POST"])
def signup():

    data = request.json

    name = data["name"]
    email = data["email"]
    password = data["password"]


    conn = get_db_connection()


    existing = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()


    if existing:

        conn.close()

        return jsonify({
            "message": "Email already exists"
        })


    password_hash = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")


    conn.execute(
        """
        INSERT INTO users
        (name, email, password_hash)

        VALUES (?, ?, ?)
        """,
        (
            name,
            email,
            password_hash
        )
    )

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]


    conn = get_db_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()


    conn.close()


    if not user:

        return jsonify({
            "message": "User not found"
        }), 404


    if bcrypt.check_password_hash(
        user["password_hash"],
        password
    ):

        return jsonify({

            "message": "Login successful",

            "user": {

                "id": user["id"],

                "name": user["name"],

                "email": user["email"]

            }

        })


    return jsonify({
        "message": "Incorrect password"
    }), 401


    conn.commit()

    conn.close()


    return jsonify({
        "message": "Signup successful"
    })

@app.route("/tbr", methods=["GET"])
def get_tbr():

    conn = get_db_connection()

    books = conn.execute(
        """
        SELECT 
            books.*
        FROM user_books

        JOIN books
        ON user_books.book_id = books.bookID

        WHERE user_books.status = 'Want to Read'
        """
    ).fetchall()


    conn.close()


    return jsonify(
        [dict(book) for book in books]
    )

@app.route("/tbr", methods=["POST"])
def add_tbr():

    data = request.json
    book_id = data["book_id"]

    conn = get_db_connection()


    existing = conn.execute(
        """
        SELECT *
        FROM user_books
        WHERE book_id = ?
        """,
        (book_id,)
    ).fetchone()


    if existing:

        conn.close()

        return jsonify(
            {"message": "Book already exists in TBR"}
        )


    conn.execute(
        """
        INSERT INTO user_books
        (book_id, status, date_added)

        VALUES (?, ?, DATE('now'))
        """,

        (
            book_id,
            "Want to Read"
        )
    )


    conn.commit()

    conn.close()


    return jsonify(
        {"message":"Book added to TBR"}
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

@app.route("/tbr/<int:book_id>", methods=["DELETE"])
def remove_tbr(book_id):

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM user_books
        WHERE book_id = ?
        """,
        (book_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Book removed from TBR"
    })

if __name__ == "__main__":
    app.run(debug=True)