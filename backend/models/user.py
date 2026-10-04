
import os
import sqlite3
import hashlib
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash


# ======================================================
# DATABASE CONFIGURATION
# ======================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    os.path.join(BASE_DIR, "interviewiq.db")
)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# ======================================================
# CREATE USERS TABLE
# ======================================================

def create_users_table():

    connection = get_connection()

    try:
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
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            hashed_password,
            education,
            skills,
            student_id
        ))

        user_id = cursor.lastrowid

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
            WHERE LOWER(email) = LOWER(?)
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
            WHERE id = ?
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
            SET student_id = ?
            WHERE id = ?
        """, (
            student_id,
            user_id
        ))

        connection.commit()

    finally:
        connection.close()


# ======================================================
# UPDATE USER PASSWORD
# ======================================================

def update_user_password(user_id, new_password):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        hashed_password = generate_password_hash(new_password)

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (
            hashed_password,
            user_id
        ))

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# ======================================================
# PASSWORD RESET TOKEN STORAGE
# ======================================================

def create_password_reset_table():

    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token_hash TEXT NOT NULL UNIQUE,
                expires_at TEXT NOT NULL,
                used INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.commit()

    finally:
        connection.close()


def save_password_reset_token(user_id, token, expires_at):

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO password_reset_tokens (
                user_id,
                token_hash,
                expires_at
            )
            VALUES (?, ?, ?)
        """, (
            user_id,
            token_hash,
            expires_at
        ))

        connection.commit()

    finally:
        connection.close()


def reset_password_with_token(token, new_password):

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    now = datetime.now(timezone.utc).isoformat()

    hashed_password = generate_password_hash(new_password)

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, user_id
            FROM password_reset_tokens
            WHERE token_hash = ?
              AND used = 0
              AND expires_at > ?
        """, (
            token_hash,
            now
        ))

        reset_record = cursor.fetchone()

        if not reset_record:
            return False

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE id = ?
        """, (
            hashed_password,
            reset_record["user_id"]
        ))

        cursor.execute("""
            UPDATE password_reset_tokens
            SET used = 1
            WHERE id = ?
        """, (reset_record["id"],))

        connection.commit()

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()