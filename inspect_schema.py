
import sqlite3

database_files = [
    "interviewiq.db",
    "backend/models/interviewiq.db"
]

for db_path in database_files:
    print("\n" + "=" * 45)
    print("DATABASE:", db_path)
    print("=" * 45)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
    """)

    tables = cursor.fetchall()

    for (table_name,) in tables:
        print(f"\nTable: {table_name}")

        cursor.execute(f'PRAGMA table_info("{table_name}")')

        columns = cursor.fetchall()

        for column in columns:
            print(
                "Column:", column[1],
                "| Type:", column[2],
                "| Primary Key:", column[5]
            )

    connection.close()