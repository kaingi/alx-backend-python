#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # This will be assigned to the variable in 'with' block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# Usage of the custom context manager
if __name__ == "__main__":
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
