import sqlite3
from werkzeug.security import generate_password_hash


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect('spendly.db')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    """Create users and expenses tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


def seed_db():
    """Insert demo user and sample expenses if database is empty."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already has data
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insert demo user
    cursor.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@spendly.com', generate_password_hash('demo123'))
    )

    # Get the demo user's id
    user_id = cursor.lastrowid

    # Insert 8 sample expenses across all categories
    sample_expenses = [
        (user_id, 45.99, 'Food', '2026-04-01', 'Grocery shopping'),
        (user_id, 25.00, 'Transport', '2026-04-03', 'Bus pass'),
        (user_id, 120.00, 'Bills', '2026-04-05', 'Electricity bill'),
        (user_id, 75.50, 'Health', '2026-04-08', 'Pharmacy'),
        (user_id, 15.99, 'Entertainment', '2026-04-10', 'Movie tickets'),
        (user_id, 89.00, 'Shopping', '2026-04-12', 'New headphones'),
        (user_id, 32.50, 'Food', '2026-04-15', 'Restaurant dinner'),
        (user_id, 50.00, 'Other', '2026-04-18', 'Gift for friend'),
    ]

    cursor.executemany(
        'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
        sample_expenses
    )

    conn.commit()
    conn.close()