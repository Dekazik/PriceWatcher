import sqlite3

DB_NAME = "price_watcher.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            url TEXT,
            selector TEXT,
            target_price REAL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def add_product(name, url, selector, target_price):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO products (name, url, selector, target_price) VALUES (?, ?, ?, ?)",
        (name, url, selector, target_price)
    )

    conn.commit()
    conn.close()



def get_all_products():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id, name, url, selector, target_price FROM products")
    rows = cur.fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "name": r[1],
            "url": r[2],
            "selector": r[3],
            "target_price": r[4]
        }
        for r in rows
    ]


def save_price(product_id, price):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO price_history (product_id, price) VALUES (?, ?)",
        (product_id, price)
    )

    conn.commit()
    conn.close()
