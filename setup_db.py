import sqlite3

conn = sqlite3.connect("business.db")
c = conn.cursor()

# Create stocks table
c.execute("""
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    quantity INTEGER,
    date TEXT
)
""")

# Create debts table
c.execute("""
CREATE TABLE IF NOT EXISTS debts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    amount REAL,
    status TEXT DEFAULT 'unpaid',
    date TEXT
)
""")

conn.commit()
conn.close()
print("Database and tables created successfully.")