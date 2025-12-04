from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if not exist
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

    db.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """)

    default_categories = ["Food", "Bills", "Transport", "Shopping", "Groceries", "Health", "Subscriptions", "Savings", "Miscellaneous"]
    for category in default_categories:
        try:
            db.execute("INSERT INTO categories (name) VALUES (?)", (category,))
        except:
            pass


# ------------------ HOME → REDIRECT TO DASHBOARD ------------------
@app.route("/")
def home():
    return redirect(url_for("dashboard"))


# ------------------ HISTORY PAGE (TRANSACTIONS TABLE) ------------------
@app.route("/history")
def history():
    db = get_db()

    search = request.args.get("search", "")
    filter_category = request.args.get("filter_category", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if search:
        query += " AND (note LIKE ? OR category LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if filter_category:
        query += " AND category = ?"
        params.append(filter_category)

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND date <= ?"
        params.append(end_date)

    query += " ORDER BY date DESC"
    transactions = db.execute(query, params).fetchall()

    categories = db.execute("SELECT * FROM categories ORDER BY name ASC").fetchall()

    return render_template("history.html",
                           transactions=transactions,
                           search=search,
                           filter_category=filter_category,
                           start_date=start_date,
                           end_date=end_date,
                           categories=categories)


# ------------------ DASHBOARD PAGE ------------------
@app.route("/dashboard")
def dashboard():
    db = get_db()

    # Monthly totals for bar chart
    monthly_data = db.execute("""
        SELECT substr(date, 1, 7) AS month, SUM(amount) AS total
        FROM transactions
        GROUP BY month
        ORDER BY month ASC
    """).fetchall()

    months = [row["month"] for row in monthly_data]
    month_totals = [row["total"] for row in monthly_data]

    # Daily spending trend
    daily_data = db.execute("""
        SELECT date, SUM(amount) AS total
        FROM transactions
        GROUP BY date
        ORDER BY date ASC
    """).fetchall()

    days = [row["date"] for row in daily_data]
    day_totals = [row["total"] for row in daily_data]

    # Category pie chart
    cat_data = db.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()

    labels = [row["category"] for row in cat_data]
    values = [row["total"] for row in cat_data]

    # Summary Card Values
    total = db.execute("SELECT SUM(amount) FROM transactions").fetchone()[0] or 0
    current_month = datetime.now().strftime("%Y-%m")
    monthly_total = db.execute("SELECT SUM(amount) FROM transactions WHERE date LIKE ?", (f"%{current_month}%",)).fetchone()[0] or 0
    top_category_row = db.execute("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        GROUP BY category
        ORDER BY total DESC LIMIT 1
    """).fetchone()
    top_category = top_category_row["category"] if top_category_row else "None"

    return render_template("dashboard.html",
                           months=months, month_totals=month_totals,
                           days=days, day_totals=day_totals,
                           labels=labels, values=values,
                           total=total, monthly_total=monthly_total, top_category=top_category)


# ------------------ ADD TRANSACTION ------------------
@app.route("/add", methods=["GET","POST"])
def add():
    db = get_db()

    if request.method == "POST":
        db.execute(
            "INSERT INTO transactions (date, category, amount, note) VALUES (?,?,?,?)",
            (request.form["date"], request.form["category"], request.form["amount"], request.form["note"])
        )
        db.commit()
        return redirect("/history?toast=added")

    categories = db.execute("SELECT * FROM categories ORDER BY name ASC").fetchall()

    selected = request.args.get("selected", "")
    date = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    amount = request.args.get("amount", "")
    note = request.args.get("note", "")

    return render_template("add.html", categories=categories, selected=selected, date=date, amount=amount, note=note)


# ------------------ EDIT ------------------
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):
    db = get_db()

    if request.method == "POST":
        db.execute("""
        UPDATE transactions SET date=?, category=?, amount=?, note=? WHERE id=?
        """, (request.form["date"], request.form["category"], request.form["amount"], request.form["note"], id))
        db.commit()
        return redirect("/history?toast=updated")

    transaction = db.execute("SELECT * FROM transactions WHERE id=?", (id,)).fetchone()
    return render_template("edit.html", transaction=transaction)


# ------------------ DELETE ------------------
@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM transactions WHERE id=?", (id,))
    db.commit()
    return redirect("/history?toast=deleted")


# ------------------ ADD CATEGORY ------------------
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


# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(debug=True)
