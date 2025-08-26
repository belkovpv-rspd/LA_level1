"""
Данный модуль для работы с БД
https://thecode.media/sqlite-py/
https://proproprogs.ru/modules/metody-fetchall-fetchmany-fetchone-iterdump

"""

import sqlite3
import csv
from datetime import datetime
from typing import List, Dict, Union
from models import Product, Client, Order

database_name = "eshop.db"


def create_tables():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            registration_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients (client_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_products (
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id),
            PRIMARY KEY (order_id, product_id)
        )
    """)

    conn.commit()
    conn.close()

def add_client(client: Client):
    """ добавляем клиента в БД"""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clients (first_name, last_name, email, phone, address, registration_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (client.first_name, client.last_name, client.email, client.phone, client.address,
          client.registration_date.isoformat()))

    client.client_id = cursor.lastrowid  # получаем айди клиента
    conn.commit()
    conn.close()

def get_all_clients() -> List[Client]:
    """список всех клиентов из БД"""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()

    clients = []

    for row in rows:
        client_id, first_name, last_name, email, phone, address, registration_date = row
        client = Client(first_name, last_name, email, phone, address)
        client.client_id = client_id
        client.registration_date = datetime.fromisoformat(registration_date)
        clients.append(client)

    conn.close()
    return clients

def delete_client(client_id: int):
    """Удаляет клиента по ID"""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM clients WHERE client_id = ?', (client_id,))
    conn.commit()
    conn.close()

def update_client(client_id: int, first_name: str, last_name: str, email: str, phone: str, address: str):
    """Обновляет данные клиента"""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE clients 
    SET first_name = ?, last_name = ?, email = ?, phone = ?, address = ?
    WHERE client_id = ?
    ''', (first_name, last_name, email, phone, address, client_id))

    conn.commit()
    conn.close()

def search_clients(search_text: str) -> List[Client]:
    """Ищет клиентов по всем полям"""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    search_pattern = f'%{search_text}%'
    cursor.execute('''
    SELECT * FROM clients 
    WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR phone LIKE ? OR address LIKE ?
    ORDER BY last_name, first_name
    ''', (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))

    rows = cursor.fetchall()
    clients = []

    for row in rows:
        client_id, first_name, last_name, email, phone, address, registration_date = row
        client = Client(first_name, last_name, email, phone, address)
        client.client_id = client_id
        client.registration_date = datetime.fromisoformat(registration_date)
        clients.append(client)

    conn.close()
    return clients

def add_product(product: Product):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO products (name, description, price)
    VALUES (?, ?, ?)
    """, (product.name, product.description, product.price))

    product.product_id = cursor.lastrowid
    conn.commit()
    conn.close()

def get_all_products() -> List[Product]:
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    products = []

    for row in rows:
        product_id, name, description, price = row
        product = Product(name, description, price)
        product.product_id = product_id
        products.append(product)

    conn.close()
    return products

def delete_product(product_id: int):
    """Удаляет товар по ID"""
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()

def add_order(order: Order):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO orders (client_id, order_date, status)
    VALUES (?, ?, ?)
    """, (order.client.client_id, order.order_date.isoformat(), order.status))

    order.order_id = cursor.lastrowid

    for product in order.products:
        cursor.execute("""
        INSERT INTO order_products (order_id, product_id)
        VALUES (?, ?)
        """, (order.order_id, product.product_id))

    conn.commit()
    conn.close()

def get_all_orders() -> List[Order]:
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()

    orders = []

    for row in rows:
        order_id, client_id, order_date, status = row

        client = get_client_by_id(client_id)
        products = get_products_by_order_id(order_id)

        order = Order(client, products, status)
        order.order_id = order_id
        order.order_date = datetime.fromisoformat(order_date)
        orders.append(order)

    conn.close()
    return orders

def get_client_by_id(client_id: int) -> Client:
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,))
    row = cursor.fetchone()

    if row:
        client_id, first_name, last_name, email, phone, address, registration_date = row
        client = Client(first_name, last_name, email, phone, address)
        client.client_id = client_id
        client.registration_date = datetime.fromisoformat(registration_date)
        conn.close()
        return client
    else:
        conn.close()
        return None

def get_products_by_order_id(order_id: int) -> List[Product]:
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT products.*
        FROM products
        JOIN order_products ON products.product_id = order_products.product_id
        WHERE order_products.order_id = ?
       """, (order_id,))
    rows = cursor.fetchall()

    products = []
    for row in rows:
        product_id, name, description, price = row
        product = Product(name, description, price)
        product.product_id = product_id
        products.append(product)

    conn.close()
    return products

def export_to_csv(filename: str):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    tables = ['clients', 'products', 'orders', 'order_products']
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        cursor.execute(f"PRAGMA table_info({table})")
        columns_info = cursor.fetchall()
        column_names = [column[1] for column in columns_info]

        with open(f"{filename}_{table}.csv", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)
            writer.writerows(rows)

    conn.close()

def import_from_csv(filename: str):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    tables = ['clients', 'products', 'orders', 'order_products']
    for table in tables:
        try:
            with open(f"{filename}_{table}.csv", 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)
                for row in reader:
                    if table == 'clients':
                        cursor.execute("""
                            INSERT INTO clients (first_name, last_name, email, phone, address, registration_date)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, row)
                    elif table == 'products':
                        cursor.execute("""
                            INSERT INTO products (name, description, price)
                            VALUES (?, ?, ?)
                        """, row)
                    elif table == 'orders':
                        cursor.execute("""
                            INSERT INTO orders (client_id, order_date, status)
                            VALUES (?, ?, ?)
                        """, row)
                    elif table == 'order_products':
                        cursor.execute("""
                            INSERT INTO order_products (order_id, product_id)
                            VALUES (?, ?)
                        """, row)
        except FileNotFoundError:
            print(f"Файл {filename}_{table}.csv не найден, пропускаем")

    conn.commit()
    conn.close()

# Инициализация базы данных при импорте
create_tables()
