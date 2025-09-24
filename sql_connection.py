import sqlite3
'''This function is for the sqlite connection'''
def get_connection(db_path):
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(f"SQLite Connection Error : {e}")
        return None
        