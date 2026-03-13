import sqlite3

# Delete all menus
conn = sqlite3.connect('yumpooma.db')
conn.execute('DELETE FROM menus')
conn.commit()
conn.close()

print("All menus deleted. Now run: python reset_ids.py menus")