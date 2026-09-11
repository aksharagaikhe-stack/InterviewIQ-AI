import os

import psycopg
from psycopg.rows import dict_row


# ======================================================
# DATABASE CONNECTION
# ======================================================

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is not configured."
        )

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


# ======================================================
# STUDENT TABLE
# ======================================================

def create_table():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
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

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO students (
                name,
                email,
                education,
                skills,
                projects
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            name,
            email,
            education,
            skills,
            projects
        ))

        student_id = cursor.fetchone()["id"]

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

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM students
            WHERE id = %s
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

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interview_history (
                id SERIAL PRIMARY KEY,

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
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING id
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

        history_id = cursor.fetchone()["id"]

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

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM interview_history
            WHERE student_id = %s
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

        cursor = connection.cursor()

        cursor.execute("""
            ALTER TABLE interview_history
            ADD COLUMN IF NOT EXISTS category TEXT
        """)

        connection.commit()

    finally:

        connection.close()