
import sqlite3
import os

databases = [
    "live_interviewiq.db",
    "live_before_migration.db",
    "live_migration.db",
]

for db_path in databases:
    print(f"\n{'=' * 45}")
    print("DATABASE:", db_path)

    if not os.path.exists(db_path):
        print("File not found.")
        continue

    try:
        # Open read-only so the downloaded copy is not modified.
        conn = sqlite3.connect(
            f"file:{os.path.abspath(db_path)}?mode=ro",
            uri=True
        )
        cursor = conn.cursor()

        tables = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
        """).fetchall()

        print("Tables:", [table[0] for table in tables])

        for (table_name,) in tables:
            if table_name in ("users", "students", "interview_history"):
                count = cursor.execute(
                    f'SELECT COUNT(*) FROM "{table_name}"'
                ).fetchone()[0]
                print(f"{table_name}: {count} records")

        conn.close()

    except sqlite3.Error as error:
        print("Database error:", error)
