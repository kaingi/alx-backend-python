#!/usr/bin/env python3
import sqlite3
import functools
from datetime import datetime  # Required for timestamping

# Decorator to log SQL queries with a timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else None
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if query:
            print(f"[{timestamp}] Executing query: {query}")
        else:
            print(f"[{timestamp}] No query provided.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Test the decorator
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
