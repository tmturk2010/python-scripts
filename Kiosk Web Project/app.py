import copy
from flask import Flask, request, render_template, redirect, url_for, session
from functools import wraps
import sqlite3
import os
import json
import datetime

app = Flask(__name__)
app.secret_key = "topraks-secret-key"

menu_items = [
    {"id": 1, "name": "Pizza", "price": 120},
    {"id": 2, "name": "Hamburger", "price": 90},
    {"id": 3, "name": "Lahmacun", "price": 50},
]

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Decorator for admin login required
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

DB_PATH = os.path.join(os.path.dirname(__file__), 'kiosk.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS staff (
        table_number INTEGER PRIMARY KEY,
        password TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_number INTEGER NOT NULL,
        items TEXT NOT NULL,
        total REAL NOT NULL,
        timestamp TEXT NOT NULL
    )''')
    # Example: insert tables 1-5 with password '1234' if not exists
    for i in range(1, 6):
        c.execute('INSERT OR IGNORE INTO staff (table_number, password) VALUES (?, ?)', (i, '1234'))
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/product")
def product():
    return render_template("product.html") 

@app.route("/menu")
def menu():
    return render_template("menu.html", menu=menu_items)

@app.route("/cart")
def cart():
    cart_items = []
    total = 0
    # Ensure cart is always a dictionary
    if "cart" not in session or not isinstance(session["cart"], dict):
        session["cart"] = {}
    for item_id, quantity in session["cart"].items():
        for item in menu_items:
            if item["id"] == int(item_id):
                item_copy = item.copy()
                item_copy["quantity"] = quantity
                cart_items.append(item_copy)
                total += item["price"] * quantity
    return render_template("cart.html", cart=cart_items, total=total)

@app.route("/add_to_cart/<int:item_id>")
def add_to_cart(item_id):
    if "cart" not in session or not isinstance(session["cart"], dict):
        session["cart"] = {}
    cart = session["cart"]
    if str(item_id) in cart:
        cart[str(item_id)] += 1
    else:
        cart[str(item_id)] = 1
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        table_number = request.form.get("table_number")
        if table_number and table_number.isdigit():
            session["table"] = int(table_number)
            return redirect(url_for("menu"))
        else:
            error = "Geçerli bir masa numarası girin."
    return render_template("login.html", error=error)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    # Only allow logout if logged in as a table
    if "table" not in session:
        return redirect(url_for("login"))
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        table_number = session.get("table")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT password FROM staff WHERE table_number = ?', (table_number,))
        row = c.fetchone()
        conn.close()
        if row and password == row["password"]:
            session.pop("table", None)
            session.pop("cart", None)
            return redirect(url_for("login"))
        else:
            error = "Şifre yanlış. Lütfen tekrar deneyin."
    return render_template("logout.html", error=error)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_panel"))
        else:
            error = "Hatalı kullanıcı adı veya şifre."
    return render_template("admin_login.html", error=error)

@app.route("/admin_logout", methods=["GET"])
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

@app.route("/admin_panel")
@admin_login_required
def admin_panel():
    return render_template("admin_panel.html")

@app.route("/submit_order", methods=["POST"])
def submit_order():
    if "table" not in session or "cart" not in session or not session["cart"]:
        return redirect(url_for("cart"))
    table_number = session["table"]
    cart_items = []
    total = 0
    for item_id, quantity in session["cart"].items():
        for item in menu_items:
            if item["id"] == int(item_id):
                item_copy = item.copy()
                item_copy["quantity"] = quantity
                cart_items.append(item_copy)
                total += item["price"] * quantity
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO orders (table_number, items, total, timestamp) VALUES (?, ?, ?, ?)',
              (table_number, json.dumps(cart_items, ensure_ascii=False), total, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()
    session.pop("cart", None)
    return redirect(url_for("menu"))

@app.route("/orders")
def orders():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM orders ORDER BY timestamp DESC')
    orders = c.fetchall()
    conn.close()
    # Parse items JSON for each order
    parsed_orders = []
    for order in orders:
        parsed_orders.append({
            "id": order["id"],
            "table_number": order["table_number"],
            "items": json.loads(order["items"]),
            "total": order["total"],
            "timestamp": order["timestamp"]
        })
    return render_template("orders.html", orders=parsed_orders)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")