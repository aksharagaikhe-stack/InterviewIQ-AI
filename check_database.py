
import sqlite3
import os

database_files = [
    "interviewiq.db",
    "backend/models/interviewiq.db"
]

for db_path in database_files:
    print("\nDatabase:", db_path)

    if not os.path.exists(db_path):
        print("File not found")
        continue

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
    """)

    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        cursor.execute(
            f'SELECT COUNT(*) FROM "{table_name}"'
        )

        count = cursor.fetchone()[0]

        print(f"{table_name}: {count} records")

    connection.close()
    