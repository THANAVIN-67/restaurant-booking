from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import sqlite3
from contextlib import closing
import json


@dataclass
class Menu:
    id: int
    name: str
    price: float
    description: Optional[str]
    image: Optional[str]
    category: str


@dataclass
class CartItem:
    id: int
    name: str
    price: float
    quantity: int


@dataclass
class Reservation:
    id: int
    name: str
    phone: str
    date: str
    time: str
    table_no: int
    people: int
    status: Optional[str] = None


@dataclass
class Bill:
    id: int
    table_no: int
    bill_time: str
    items: List[Dict[str, Any]]
    total: float


@dataclass
class Sale:
    id: int
    sale_date: str
    menu_id: int
    quantity: int
    total_price: float


@dataclass
class Admin:
    id: int
    username: str
    password: str


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_menus(self) -> List[Dict[str, Any]]:
        with closing(self._connect()) as conn:
            rows = conn.execute('SELECT * FROM menus').fetchall()
            return [dict(r) for r in rows]

    def get_menu(self, menu_id: int) -> Optional[Dict[str, Any]]:
        with closing(self._connect()) as conn:
            row = conn.execute('SELECT * FROM menus WHERE id=?', (menu_id,)).fetchone()
            return dict(row) if row else None

    def add_menu(self, name: str, price: float, description: Optional[str], image: Optional[str], category: str):
        with closing(self._connect()) as conn:
            conn.execute('INSERT INTO menus (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)',
                         (name, price, description, image, category))
            conn.commit()

    def update_menu(self, menu_id: int, name: str, price: float, description: Optional[str], image: Optional[str], category: str):
        with closing(self._connect()) as conn:
            conn.execute('UPDATE menus SET name=?, price=?, description=?, image=?, category=? WHERE id=?',
                         (name, price, description, image, category, menu_id))
            conn.commit()

    def delete_menu(self, menu_id: int):
        with closing(self._connect()) as conn:
            conn.execute('DELETE FROM menus WHERE id=?', (menu_id,))
            conn.commit()

    def get_reservations(self) -> List[Dict[str, Any]]:
        with closing(self._connect()) as conn:
            rows = conn.execute('SELECT * FROM reservations').fetchall()
            return [dict(r) for r in rows]

    def has_conflicting_reservation(self, date: str, table_no: int, start_time: str, end_time: str) -> bool:
        with closing(self._connect()) as conn:
            query = '''SELECT * FROM reservations WHERE date=? AND table_no=? AND ((time >= ? AND time < ?) OR (time > ? AND time <= ?))'''
            rows = conn.execute(query, (date, table_no, start_time, end_time, start_time, end_time)).fetchall()
            return len(rows) > 0

    def add_reservation(self, name: str, phone: str, date: str, time: str, table_no: int, people: int):
        with closing(self._connect()) as conn:
            conn.execute('INSERT INTO reservations (name, phone, date, time, table_no, people) VALUES (?, ?, ?, ?, ?, ?)',
                         (name, phone, date, time, table_no, people))
            conn.commit()

    def delete_reservation(self, reservation_id: int):
        with closing(self._connect()) as conn:
            conn.execute('DELETE FROM reservations WHERE id=?', (reservation_id,))
            conn.commit()

    def authenticate_admin(self, username: str, password: str) -> bool:
        with closing(self._connect()) as conn:
            row = conn.execute('SELECT * FROM admin WHERE username=? AND password=?', (username, password)).fetchone()
            return bool(row)

    def add_bill_and_sales(self, table_no: int, cart: List[Dict[str, Any]], bill_time: str):
        sale_date = bill_time[:10]
        total = sum(item['price'] * item['quantity'] for item in cart)
        items_json = json.dumps(cart, ensure_ascii=False)
        with closing(self._connect()) as conn:
            conn.execute('INSERT INTO bills (table_no, bill_time, items, total) VALUES (?, ?, ?, ?)',
                         (table_no, bill_time, items_json, total))
            for item in cart:
                conn.execute('INSERT INTO sales (sale_date, menu_id, quantity, total_price) VALUES (?, ?, ?, ?)',
                             (sale_date, item['id'], item['quantity'], item['price'] * item['quantity']))
            conn.commit()

    def get_bill(self, bill_id: int) -> Optional[Dict[str, Any]]:
        with closing(self._connect()) as conn:
            row = conn.execute('SELECT * FROM bills WHERE id=?', (bill_id,)).fetchone()
            return dict(row) if row else None

    def get_daily_sales(self, date: str) -> Dict[str, Any]:
        with closing(self._connect()) as conn:
            row = conn.execute('SELECT SUM(total_price) as total, SUM(quantity) as qty FROM sales WHERE sale_date = ?', (date,)).fetchone()
            return dict(row) if row else {'total': 0, 'qty': 0}

    def get_monthly_sales(self) -> List[Dict[str, Any]]:
        with closing(self._connect()) as conn:
            rows = conn.execute('SELECT strftime("%Y", sale_date) as year, strftime("%m", sale_date) as month, SUM(total_price) as total, SUM(quantity) as qty FROM sales GROUP BY year, month ORDER BY year DESC, month DESC').fetchall()
            return [dict(r) for r in rows]

    def init_db(self):
        with closing(self._connect()) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS bills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_no INTEGER,
                    bill_time TEXT,
                    items TEXT,
                    total REAL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_date TEXT,
                    menu_id INTEGER,
                    quantity INTEGER,
                    total_price REAL
                )
            ''')
            # Note: other tables (menus, reservations, admin) assumed to exist already in user's DB
            conn.commit()
