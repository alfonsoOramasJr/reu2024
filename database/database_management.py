import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def create_tables_if_not_exist():
    tables = ["thumb", "index_finger", "middle_finger", "ring_finger", "pinky"]
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    for table in tables:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            data BLOB
        )
        """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables_if_not_exist()
