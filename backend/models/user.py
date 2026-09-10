import os
import sqlite3

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "interviewiq.db")


# ======================================================
# DATABASE
# ======================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE = os.path.join(
    BASE_DIR,
    "interviewiq.db"
)


# ======================================================
# DATABASE CONNECTION
# ======================================================

def get_connection():
    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# ======================================================
# CREATE USERS TABLE
# ======================================================

def create_users_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            password TEXT NOT NULL,

            education TEXT,

            skills TEXT,

            student_id INTEGER,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Check existing columns
    cursor.execute(
        "PRAGMA table_info(users)"
    )

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    # Add student_id if missing
    if "student_id" not in columns:

        cursor.execute("""
            ALTER TABLE users
            ADD COLUMN student_id INTEGER
        """)

    connection.commit()

    connection.close()


# ======================================================
# CREATE USER
# ======================================================

def create_user(
    name,
    email,
    password,
    education,
    skills,
    student_id=None
):

    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = generate_password_hash(
        password
    )

    cursor.execute("""
        INSERT INTO users
        (
            name,
            email,
            password,
            education,
            skills,
            student_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        hashed_password,
        education,
        skills,
        student_id
    ))

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


# ======================================================
# GET USER BY EMAIL
# ======================================================

def get_user_by_email(email):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    connection.close()

    return user


# ======================================================
# VERIFY PASSWORD
# ======================================================

def verify_password(
    stored_password,
    entered_password
):

    return check_password_hash(
        stored_password,
        entered_password
    )


# ======================================================
# GET USER
# ======================================================

def get_user(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    connection.close()

    return user


# ======================================================
# UPDATE STUDENT ID
# ======================================================

def update_user_student_id(
    user_id,
    student_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET student_id = ?
        WHERE id = ?
    """, (
        student_id,
        user_id
    ))

    connection.commit()

    connection.close()