
from flask import Blueprint, request, jsonify
import sqlite3
import secrets

from datetime import datetime, timedelta, timezone

from models.user import (
    create_user,
    get_user_by_email,
    verify_password,
    get_user,
    update_user_student_id,
    save_password_reset_token,
    reset_password_with_token
)

from models.student import (
    create_student,
    get_connection
)


# ======================================================
# AUTH BLUEPRINT
# ======================================================

auth_bp = Blueprint("auth", __name__)


# ======================================================
# SIGNUP
# ======================================================

@auth_bp.route("/api/signup", methods=["POST"])
def signup():

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()
    education = data.get("education", "").strip()
    skills = data.get("skills", "").strip()

    if not name:
        return jsonify({
            "success": False,
            "message": "Name is required."
        }), 400

    if not email:
        return jsonify({
            "success": False,
            "message": "Email is required."
        }), 400

    if not password:
        return jsonify({
            "success": False,
            "message": "Password is required."
        }), 400

    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must be at least 6 characters."
        }), 400

    try:

        # Check whether account already exists
        existing_user = get_user_by_email(email)

        if existing_user:
            return jsonify({
                "success": False,
                "message": "An account with this email already exists."
            }), 409

        # Create student profile
        student_id = create_student(
            name,
            email,
            education,
            skills,
            ""
        )

        # Create user account
        user_id = create_user(
            name,
            email,
            password,
            education,
            skills,
            student_id
        )

        return jsonify({
            "success": True,
            "message": "Account created successfully!",
            "user_id": user_id,
            "student_id": student_id
        }), 201

    except sqlite3.IntegrityError:

        return jsonify({
            "success": False,
            "message": "An account with this email already exists."
        }), 409

    except Exception as error:

        print("SIGNUP ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to create account. Please try again."
        }), 500


# ======================================================
# LOGIN
# ======================================================

@auth_bp.route("/api/login", methods=["POST"])
def login():

    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email:
        return jsonify({
            "success": False,
            "message": "Email is required."
        }), 400

    if not password:
        return jsonify({
            "success": False,
            "message": "Password is required."
        }), 400

    try:

        # Find user
        user = get_user_by_email(email)

        if user is None:
            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        # Verify password
        if not verify_password(
            password,
            user["password"]
        ):
            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        student_id = user["student_id"]

        # Support older accounts without student_id
        if student_id is None:

            connection = get_connection()

            try:
                cursor = connection.cursor()

                cursor.execute("""
                    SELECT *
                    FROM students
                    WHERE LOWER(email) = LOWER(?)
                """, (user["email"],))

                existing_student = cursor.fetchone()

            finally:
                connection.close()

            if existing_student:
                student_id = existing_student["id"]

            else:
                student_id = create_student(
                    user["name"],
                    user["email"],
                    user["education"] or "",
                    user["skills"] or "",
                    ""
                )

            update_user_student_id(
                user["id"],
                student_id
            )

        return jsonify({
            "success": True,
            "message": "Login successful!",
            "user": {
                "id": user["id"],
                "student_id": student_id,
                "name": user["name"],
                "email": user["email"],
                "education": user["education"],
                "skills": user["skills"]
            }
        }), 200

    except Exception as error:

        print("LOGIN ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to login. Please try again."
        }), 500


# ======================================================
# GET USER PROFILE
# ======================================================

@auth_bp.route(
    "/api/user/<int:user_id>",
    methods=["GET"]
)
def get_user_profile(user_id):

    try:

        user = get_user(user_id)

        if user is None:
            return jsonify({
                "success": False,
                "message": "User not found."
            }), 404

        return jsonify({
            "success": True,
            "user": {
                "id": user["id"],
                "student_id": user["student_id"],
                "name": user["name"],
                "email": user["email"],
                "education": user["education"],
                "skills": user["skills"]
            }
        }), 200

    except Exception as error:

        print("PROFILE ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to retrieve user profile."
        }), 500


# ======================================================
# FORGOT PASSWORD
# ======================================================

@auth_bp.route("/api/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()

    if not email:
        return jsonify({
            "success": False,
            "message": "Email is required."
        }), 400

    try:
        user = get_user_by_email(email)

        if user is None:
            return jsonify({
                "success": True,
                "message": "If the account exists, password recovery can proceed."
            }), 200

        token = secrets.token_urlsafe(32)

        expires_at = (
            datetime.now(timezone.utc) + timedelta(minutes=15)
        ).isoformat()

        save_password_reset_token(
            user["id"],
            token,
            expires_at
        )

        # LOCAL DEVELOPMENT ONLY:
        # Do not expose reset tokens in production.
        return jsonify({
            "success": True,
            "message": "Reset token generated for local testing.",
            "reset_token": token
        }), 200

    except Exception as error:

        print("FORGOT PASSWORD ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to process password recovery."
        }), 500


# ======================================================
# RESET PASSWORD
# ======================================================

@auth_bp.route("/api/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json() or {}

    token = data.get("token", "").strip()
    new_password = data.get("new_password", "")

    if not token or not new_password:
        return jsonify({
            "success": False,
            "message": "Token and new password are required."
        }), 400

    if len(new_password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must be at least 6 characters."
        }), 400

    try:
        success = reset_password_with_token(
            token,
            new_password
        )

        if not success:
            return jsonify({
                "success": False,
                "message": "Invalid, expired, or already used reset token."
            }), 400

        return jsonify({
            "success": True,
            "message": "Password reset successfully. Please login."
        }), 200

    except Exception as error:

        print("RESET PASSWORD ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to reset password."
        }), 500