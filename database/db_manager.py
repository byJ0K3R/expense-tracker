import sqlite3
import os

DB_PATH = os.path.join(os.path.expanduser("~"), "expenses.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(amount, category, date, comment=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount, category, date, comment) VALUES (?, ?, ?, ?)",
        (amount, category, date, comment)
    )
    conn.commit()
    conn.close()

def get_expenses(month=None, year=None):
    conn = get_connection()
    cursor = conn.cursor()
    if month and year:
        pattern = f"{year}-{month:02d}-%"
        cursor.execute(
            "SELECT * FROM expenses WHERE date LIKE ? ORDER BY date DESC",
            (pattern,)
        )
    else:
        cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
