from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- Home route ---
@app.route("/", methods=["GET"])
def home():
    conn = sqlite3.connect("business.db")
    conn.row_factory = sqlite3.Row  # ← This makes fetch results accessible by column name
    c = conn.cursor()

    # Get all stocks
    c.execute("SELECT * FROM stocks ORDER BY date DESC")
    stocks_list = c.fetchall()

    # Get all debts
    c.execute("SELECT * FROM debts ORDER BY date DESC")
    debts_list = c.fetchall()

    conn.close()
    return render_template("home.html", stocks=stocks_list, debts=debts_list)

# --- Add stock ---
@app.route("/stocks", methods=["POST"])
def add_stock():
    conn = sqlite3.connect("business.db")
    c = conn.cursor()
    item = request.form["item"]
    quantity = request.form["quantity"]
    date = request.form["date"]
    c.execute("INSERT INTO stocks (item, quantity, date) VALUES (?, ?, ?)", (item, quantity, date))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# --- Add debt ---
@app.route("/debts", methods=["POST"])
def add_debt():
    conn = sqlite3.connect("business.db")
    c = conn.cursor()
    name = request.form["name"]
    amount = request.form["amount"]
    date = request.form["date"]
    c.execute("INSERT INTO debts (name, amount, date) VALUES (?, ?, ?)", (name, amount, date))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# --- Mark debt paid ---
@app.route("/pay_debt/<int:debt_id>", methods=["POST"])
def pay_debt(debt_id):
    conn = sqlite3.connect("business.db")
    c = conn.cursor()
    c.execute("UPDATE debts SET status='paid' WHERE id=?", (debt_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# --- Delete stock ---
@app.route("/delete_stock/<int:stock_id>", methods=["POST"])
def delete_stock(stock_id):
    conn = sqlite3.connect("business.db")
    c = conn.cursor()
    c.execute("DELETE FROM stocks WHERE id=?", (stock_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# --- Delete debt ---
@app.route("/delete_debt/<int:debt_id>", methods=["POST"])
def delete_debt(debt_id):
    conn = sqlite3.connect("business.db")
    c = conn.cursor()
    c.execute("DELETE FROM debts WHERE id=?", (debt_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# --- Run server ---
if __name__ == "__main__":
    app.run()