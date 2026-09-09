import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "interviewiq.db")


# ==========================================
# ============
# DATABASE CONNECTION
# ======================================================

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# ======================================================
# STUDENT TABLE
# Phase 3
# ======================================================

def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
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
    connection.close()


# ======================================================
# CREATE STUDENT
# Phase 3
# ======================================================

def create_student(
    name,
    email,
    education,
    skills,
    projects
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (
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

    connection.commit()

    student_id = cursor.lastrowid

    connection.close()

    return student_id


# ======================================================
# GET STUDENT
# Phase 3
# ======================================================

def get_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    connection.close()

    return student


# ======================================================
# INTERVIEW HISTORY TABLE
# Phase 6.3
# ======================================================

def create_interview_history_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id INTEGER NOT NULL,

            interview_type TEXT,
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
        )
    """)

    connection.commit()
    connection.close()


# ======================================================
# SAVE INTERVIEW HISTORY
# Phase 6.3
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
    cursor = connection.cursor()

    cursor.execute("""
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

    connection.commit()

    history_id = cursor.lastrowid

    connection.close()

    return history_id
# ======================================================
# GET INTERVIEW HISTORY
# Phase 6.3
# ======================================================

def get_interview_history(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM interview_history
        WHERE student_id = ?
        ORDER BY created_at DESC
    """, (student_id,))

    history = cursor.fetchall()

    connection.close()

    return history


def add_category_column():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("PRAGMA table_info(interview_history)")
    columns = [row["name"] for row in cursor.fetchall()]

    if "category" not in columns:
        cursor.execute(
            "ALTER TABLE interview_history ADD COLUMN category TEXT"
        )
        connection.commit()

    connection.close()