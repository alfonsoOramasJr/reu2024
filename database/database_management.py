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
            channel INTEGER NOT NULL,
            data_value INTEGER NOT NULL
        )
        """)

    conn.commit()
    conn.close()

def get_values_from_table(table_name, channel):
    if table_name not in ["thumb", "index_finger", "middle_finger", "ring_finger", "pinky"]:
        raise ValueError("Invalid table name. Must be one of: thumb, index_finger, middle_finger, ring_finger, pinky")
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name} WHERE channel = ?", (channel,))
    rows = cursor.fetchall()

    conn.close()
    return rows

if __name__ == "__main__":
    create_tables_if_not_exist()
    # Example usage
    # values = get_values_from_table("thumb", 1)
    # print(values)
