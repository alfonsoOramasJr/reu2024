import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect_to_db()

    def connect_to_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def create_tables_if_not_exist(self):
        tables = ["thumb", "index_finger", "middle_finger", "ring_finger", "pinky"]

        for table in tables:
            self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel INTEGER NOT NULL,
                data_value INTEGER NOT NULL
            )
            """)

        self.conn.commit()

    def get_values_from_table(self, table_name, channel):
        if table_name not in ["thumb", "index_finger", "middle_finger", "ring_finger", "pinky"]:
            raise ValueError("Invalid table name. Must be one of: thumb, index_finger, middle_finger, ring_finger, pinky")

        self.cursor.execute(f"SELECT * FROM {table_name} WHERE channel = ?", (channel,))
        rows = self.cursor.fetchall()
        return rows

    def gather_all_data(self):
        tables = ["thumb", "index_finger", "middle_finger", "ring_finger", "pinky"]
        all_data = []

        for table in tables:
            self.cursor.execute(f"SELECT DISTINCT channel FROM {table}")
            channels = [row[0] for row in self.cursor.fetchall()]
            for channel in channels:
                data = self.get_values_from_table(table, channel)
                all_data.append(data)

        return all_data

if __name__ == "__main__":
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database.db')
    db_manager = DatabaseManager(DATABASE_PATH)
    db_manager.create_tables_if_not_exist()
    # Example usage
    # values = db_manager.get_values_from_table("thumb", 1)
    # print(values)
    all_data = db_manager.gather_all_data()
    for data in all_data:
        print(data)
    db_manager.close_connection()
