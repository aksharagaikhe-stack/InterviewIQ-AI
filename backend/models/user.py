import os

import psycopg
from psycopg.rows import dict_row
from werkzeug.security import generate_password_hash, check_password_hash


# ======================================================
# DATABASE CONFIGURATION
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
# CREATE USERS TABLE
# ======================================================

def create_users_table():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                education TEXT,
                skills TEXT,
                student_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:

        connection.close()


# ======================================================
# CREATE USER
# ======================================================

def create_user(
    name,
    email,
    password,
    education=None,
    skills=None,
    student_id=None
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (
                name,
                email,
                password,
                education,
                skills,
                student_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            name,
            email,
            hashed_password,
            education,
            skills,
            student_id
        ))

        user_id = cursor.fetchone()["id"]

        connection.commit()

        return user_id

    finally:

        connection.close()


# ======================================================
# GET USER BY EMAIL
# ======================================================

def get_user_by_email(email):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                password,
                education,
                skills,
                student_id,
                created_at
            FROM users
            WHERE LOWER(email) = LOWER(%s)
        """, (email,))

        return cursor.fetchone()

    finally:

        connection.close()


# ======================================================
# VERIFY PASSWORD
# ======================================================

def verify_password(password, hashed_password):

    return check_password_hash(
        hashed_password,
        password
    )


# ======================================================
# GET USER BY ID
# ======================================================

def get_user(user_id):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                password,
                education,
                skills,
                student_id,
                created_at
            FROM users
            WHERE id = %s
        """, (user_id,))

        return cursor.fetchone()

    finally:

        connection.close()


# ======================================================
# UPDATE STUDENT ID
# ======================================================

def update_user_student_id(
    user_id,
    student_id
):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            UPDATE users
            SET student_id = %s
            WHERE id = %s
        """, (
            student_id,
            user_id
        ))

        connection.commit()

    finally:

        connection.close()