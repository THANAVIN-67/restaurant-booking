"""Utility script to reset AUTOINCREMENT counters in SQLite database.

Run this whenever you want the next inserted row for a table to start from a specific
value (e.g. 1). This is useful after deleting all rows or rebuilding data.

Usage examples:
    python reset_ids.py menus bills reservations

The script will update the `sqlite_sequence` table for each named table, setting
the sequence value to the maximum existing id (or 0 if table empty). That makes
the next inserted row have id=max+1 (so 1 when empty).

It does NOT renumber existing rows. If you want to renumber, delete and reinsert
or run custom SQL.
"""

import sqlite3
import sys

DB_PATH = 'yumpooma.db'

def reset_sequence(table_name: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # get the current max id
        cursor.execute(f"SELECT MAX(id) FROM {table_name}")
        row = cursor.fetchone()
        max_id = row[0] if row and row[0] is not None else 0
        # if table empty set seq to 0 so next id = 1
        seq_value = max_id
        cursor.execute("UPDATE sqlite_sequence SET seq=? WHERE name=?", (seq_value, table_name))
        conn.commit()
        print(f"Reset sequence for {table_name} to {seq_value} (next id will be {seq_value+1})")


def main():
    if len(sys.argv) < 2:
        print("Usage: python reset_ids.py table1 [table2 ...]")
        sys.exit(1)
    for tbl in sys.argv[1:]:
        try:
            reset_sequence(tbl)
        except Exception as e:
            print(f"Error resetting {tbl}: {e}")

if __name__ == '__main__':
    main()
