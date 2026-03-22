from __future__ import annotations

import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "sales_analytics.db"


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    segment TEXT NOT NULL,
    city TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    line_total REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
"""


CUSTOMERS = [
    (1, "Ana Souza", "Enterprise", "Sao Paulo"),
    (2, "Carlos Lima", "SMB", "Rio de Janeiro"),
    (3, "Juliana Alves", "Enterprise", "Belo Horizonte"),
    (4, "Marcos Silva", "Startup", "Curitiba"),
    (5, "Fernanda Rocha", "SMB", "Recife"),
]

PRODUCTS = [
    (1, "Analytics Cloud", "Software", 1200.0),
    (2, "SQL Copilot", "Software", 850.0),
    (3, "Onboarding Package", "Services", 400.0),
    (4, "Premium Support", "Services", 650.0),
    (5, "Data Integration API", "Platform", 980.0),
]

ORDERS = [
    (101, 1, "2025-01-15", "paid", 2050.0),
    (102, 2, "2025-01-20", "paid", 1250.0),
    (103, 3, "2025-02-03", "pending", 2180.0),
    (104, 4, "2025-02-18", "paid", 850.0),
    (105, 5, "2025-03-01", "cancelled", 400.0),
    (106, 1, "2025-03-10", "paid", 1630.0),
    (107, 3, "2025-03-12", "paid", 1850.0),
    (108, 2, "2025-03-21", "pending", 980.0),
]

ORDER_ITEMS = [
    (1001, 101, 1, 1, 1200.0),
    (1002, 101, 4, 1, 650.0),
    (1003, 101, 3, 1, 200.0),
    (1004, 102, 2, 1, 850.0),
    (1005, 102, 3, 1, 400.0),
    (1006, 103, 1, 1, 1200.0),
    (1007, 103, 5, 1, 980.0),
    (1008, 104, 2, 1, 850.0),
    (1009, 105, 3, 1, 400.0),
    (1010, 106, 5, 1, 980.0),
    (1011, 106, 4, 1, 650.0),
    (1012, 107, 1, 1, 1200.0),
    (1013, 107, 4, 1, 650.0),
    (1014, 108, 5, 1, 980.0),
]


def seed_database(db_path: Path | None = None) -> Path:
    db_path = db_path or DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for statement in SCHEMA_SQL.strip().split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)

    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM customers")

    cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", CUSTOMERS)
    cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", PRODUCTS)
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", ORDERS)
    cursor.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", ORDER_ITEMS)

    connection.commit()
    connection.close()
    return db_path


def get_connection(db_path: Path | None = None):
    return sqlite3.connect(db_path or DB_PATH)
