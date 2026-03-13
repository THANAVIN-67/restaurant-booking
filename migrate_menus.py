"""Migrate menus table to remove AUTOINCREMENT and allow ID reuse"""

import sqlite3

def migrate_menus_table():
    conn = sqlite3.connect('yumpooma.db')
    cursor = conn.cursor()

    # Backup existing data
    cursor.execute('SELECT * FROM menus')
    existing_menus = cursor.fetchall()

    # Drop and recreate table without AUTOINCREMENT
    cursor.execute('DROP TABLE menus')

    cursor.execute('''
        CREATE TABLE menus (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image TEXT,
            category TEXT NOT NULL
        )
    ''')

    # Restore data
    for menu in existing_menus:
        cursor.execute('INSERT INTO menus (id, name, price, description, image, category) VALUES (?, ?, ?, ?, ?, ?)', menu)

    # Reset sequence to 0 (will be managed by our code)
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='menus'")

    conn.commit()
    conn.close()
    print("Migration completed! Menus table now allows ID reuse.")

if __name__ == '__main__':
    migrate_menus_table()