from flask import Blueprint, request, jsonify

from models.user import (
    create_user,
    get_user_by_email,
    verify_password,
    get_user,
    update_user_student_id
)

from models.student import (
    create_student,
    get_student
)

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "interviewiq.db")


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

        # ==================================================
        # CREATE STUDENT PROFILE
        # ==================================================

        student_id = create_student(
            name,
            email,
            education,
            skills,
            ""
        )


        # ==================================================
        # CREATE USER ACCOUNT
        # ==================================================

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

        user = get_user_by_email(email)


        if user is None:

            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401


        if not verify_password(
            user["password"],
            password
        ):

            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401


        # ==================================================
        # GET STUDENT ID
        # ==================================================

        student_id = user["student_id"]


        # ==================================================
        # OLD ACCOUNT SUPPORT
        # ==================================================
        # If an account was created before the student_id
        # connection was added, create/link a student profile.

        if student_id is None:

            existing_student = None

            try:

                connection = sqlite3.connect(DATABASE)

                connection.row_factory = sqlite3.Row

                cursor = connection.cursor()

                cursor.execute("""
                    SELECT *
                    FROM students
                    WHERE email = ?
                """, (user["email"],))

                existing_student = cursor.fetchone()

                connection.close()

            except Exception as error:

                print(
                    "OLD ACCOUNT STUDENT LOOKUP ERROR:",
                    error
                )


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


        # ==================================================
        # LOGIN SUCCESS
        # ==================================================

        return jsonify({

            "success": True,

            "message": "Login successful!",

            "user": {

                "id":
                    user["id"],

                "student_id":
                    student_id,

                "name":
                    user["name"],

                "email":
                    user["email"],

                "education":
                    user["education"],

                "skills":
                    user["skills"]
            }

        }), 200


    except Exception as error:

        print("LOGIN ERROR:", error)

        return jsonify({

            "success": False,

            "message":
                "Unable to login. Please try again."

        }), 500


# ======================================================
# GET USER PROFILE
# ======================================================

@auth_bp.route(
    "/api/user/<int:user_id>",
    methods=["GET"]
)
def get_user_profile(user_id):

    user = get_user(user_id)


    if user is None:

        return jsonify({

            "success": False,

            "message":
                "User not found."

        }), 404


    return jsonify({

        "success": True,

        "user": {

            "id":
                user["id"],

            "student_id":
                user["student_id"],

            "name":
                user["name"],

            "email":
                user["email"],

            "education":
                user["education"],

            "skills":
                user["skills"]
        }

    }), 200
