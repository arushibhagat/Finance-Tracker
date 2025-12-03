from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
with get_db() as db:
    db.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT,
        amount REAL NOT NULL,
        note TEXT
    );
    """)

@app.route("/")
def index():
    db = get_db()
    transactions = db.execute("SELECT * FROM transactions ORDER BY date DESC").fetchall()
    total = db.execute("SELECT SUM(amount) FROM transactions").fetchone()[0] or 0
    return render_template("index.html", transactions=transactions, total=total)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        date = request.form["date"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        note = request.form["note"]

        db = get_db()
        db.execute("INSERT INTO transactions (date, category, amount, note) VALUES (?,?,?,?)",
                   (date, category, amount, note))
        db.commit()
        return redirect("/")
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
