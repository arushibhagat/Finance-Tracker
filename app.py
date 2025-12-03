from datetime import datetime

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
    # Create transactions table
    db.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT,
        amount REAL NOT NULL,
        note TEXT
    );
    """)

    # Create categories table
    db.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """)

    # Insert default categories if empty
    default_categories = ["Food", "Bills", "Transport", "Shopping", "Groceries", "Health", "Subscriptions", "Savings", "Miscellaneous"]
    for category in default_categories:
        try:
            db.execute("INSERT INTO categories (name) VALUES (?)", (category,))
        except:
            pass


@app.route("/")
def index():
    db = get_db()
    transactions = db.execute("SELECT * FROM transactions ORDER BY date DESC").fetchall()
    total = db.execute("SELECT SUM(amount) FROM transactions").fetchone()[0] or 0
    return render_template("index.html", transactions=transactions, total=total)

@app.route("/add", methods=["GET","POST"])
def add():
    db = get_db()

    if request.method == "POST":
        db.execute(
            "INSERT INTO transactions (date, category, amount, note) VALUES (?,?,?,?)",
            (request.form["date"], request.form["category"], request.form["amount"], request.form["note"])
        )
        db.commit()
        return redirect("/")

    categories = db.execute("SELECT * FROM categories ORDER BY name ASC").fetchall()

    # Get values preserved from redirect
    selected = request.args.get("selected", "")
    date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    amount = request.args.get("amount", "")
    note = request.args.get("note", "")

    return render_template("add.html", categories=categories, selected=selected, date=date, amount=amount, note=note)




@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM transactions WHERE id=?", (id,))
    db.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    db = get_db()

    if request.method == "POST":
        db.execute("""
            UPDATE transactions 
            SET date=?, category=?, amount=?, note=? 
            WHERE id=?
        """, (
            request.form["date"],
            request.form["category"],
            request.form["amount"],
            request.form["note"],
            id
        ))
        db.commit()
        return redirect("/")

    # Fetch existing entry for display
    transaction = db.execute("SELECT * FROM transactions WHERE id=?", (id,)).fetchone()
    return render_template("edit.html", transaction=transaction)

@app.route("/add-category", methods=["POST"])
def add_category():
    db = get_db()
    new_cat = request.form["new_category"]
    date = request.form.get("date", "")
    amount = request.form.get("amount", "")
    note = request.form.get("note", "")

    try:
        db.execute("INSERT INTO categories (name) VALUES (?)", (new_cat,))
        db.commit()
    except:
        pass

    return redirect(f"/add?selected={new_cat}&date={date}&amount={amount}&note={note}")



if __name__ == "__main__":
    app.run(debug=True)
