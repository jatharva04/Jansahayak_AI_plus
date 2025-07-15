import sqlite3

def init_db():
    conn = sqlite3.connect('complaints.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            complaint TEXT,
            category TEXT,
            location TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()
