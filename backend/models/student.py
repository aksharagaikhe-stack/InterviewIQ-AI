
import os
import sqlite3

# ======================================================
# DATABASE PATH
# ======================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATABASE_PATH = os.path.join(BASE_DIR, "interviewiq.db")


# ======================================================
# DATABASE CONNECTION
# ======================================================

def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ======================================================
# STUDENT TABLE
# ======================================================

def create_table():

    connection = get_connection()

    try:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                education TEXT,
                skills TEXT,
                projects TEXT
            )
        """)

        connection.commit()

    finally:

        connection.close()


# ======================================================
# CREATE STUDENT
# ======================================================

def create_student(
    name,
    email,
    education,
    skills,
    projects
):

    connection = get_connection()

    try:

        cursor = connection.execute("""
            INSERT INTO students (
                name,
                email,
                education,
                skills,
                projects
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            education,
            skills,
            projects
        ))

        student_id = cursor.lastrowid

        connection.commit()

        return student_id

    finally:

        connection.close()


# ======================================================
# GET STUDENT
# ======================================================

def get_student(student_id):

    connection = get_connection()

    try:

        cursor = connection.execute("""
            SELECT *
            FROM students
            WHERE id = ?
        """, (student_id,))

        return cursor.fetchone()

    finally:

        connection.close()


# ======================================================
# INTERVIEW HISTORY TABLE
# ======================================================

def create_interview_history_table():

    connection = get_connection()

    try:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS interview_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER NOT NULL,

                interview_type TEXT,
                category TEXT,
                role TEXT,
                difficulty TEXT,
                language TEXT,

                question_count INTEGER,

                overall_score REAL,
                technical_score REAL,
                communication_score REAL,
                relevance_score REAL,
                grammar_score REAL,
                clarity_score REAL,

                strengths TEXT,
                weaknesses TEXT,
                suggestions TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (student_id)
                    REFERENCES students(id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()

    finally:

        connection.close()


# ======================================================
# SAVE INTERVIEW HISTORY
# ======================================================

def save_interview_history(
    student_id,
    interview_type,
    category,
    role,
    difficulty,
    language,
    question_count,
    overall_score,
    technical_score,
    communication_score,
    relevance_score,
    grammar_score,
    clarity_score,
    strengths,
    weaknesses,
    suggestions
):

    connection = get_connection()

    try:

        cursor = connection.execute("""
            INSERT INTO interview_history (
                student_id,
                interview_type,
                category,
                role,
                difficulty,
                language,
                question_count,
                overall_score,
                technical_score,
                communication_score,
                relevance_score,
                grammar_score,
                clarity_score,
                strengths,
                weaknesses,
                suggestions
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            student_id,
            interview_type,
            category,
            role,
            difficulty,
            language,
            question_count,
            overall_score,
            technical_score,
            communication_score,
            relevance_score,
            grammar_score,
            clarity_score,
            strengths,
            weaknesses,
            suggestions
        ))

        history_id = cursor.lastrowid

        connection.commit()

        return history_id

    finally:

        connection.close()


# ======================================================
# GET INTERVIEW HISTORY
# ======================================================

def get_interview_history(student_id):

    connection = get_connection()

    try:

        cursor = connection.execute("""
            SELECT *
            FROM interview_history
            WHERE student_id = ?
            ORDER BY created_at DESC
        """, (student_id,))

        return cursor.fetchall()

    finally:

        connection.close()


# ======================================================
# CATEGORY COLUMN
# ======================================================

def add_category_column():

    connection = get_connection()

    try:

        columns = connection.execute(
            "PRAGMA table_info(interview_history)"
        ).fetchall()

        column_names = [column["name"] for column in columns]

        if "category" not in column_names:

            connection.execute("""
                ALTER TABLE interview_history
                ADD COLUMN category TEXT
            """)

            connection.commit()

    finally:

        connection.close()