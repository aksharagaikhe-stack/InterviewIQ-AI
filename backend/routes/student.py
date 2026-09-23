from flask import Blueprint, request, jsonify

from models.student import (
    create_student,
    get_student,
    get_connection
)

import psycopg


student_bp = Blueprint("student", __name__)


# ======================================================
# CREATE / UPDATE STUDENT PROFILE
# ======================================================

@student_bp.route("/api/student", methods=["POST"])
def create_student_profile():

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
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

    try:

        # --------------------------------------------------
        # CHECK IF STUDENT ALREADY EXISTS
        # --------------------------------------------------

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT id
                FROM students
                WHERE LOWER(email) = LOWER(%s)
            """, (email,))

            existing_student = cursor.fetchone()

        finally:
            connection.close()


        # --------------------------------------------------
        # UPDATE EXISTING STUDENT
        # --------------------------------------------------

        if existing_student:

            student_id = existing_student["id"]

            connection = get_connection()

            try:
                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE students
                    SET
                        name = %s,
                        education = %s,
                        skills = %s
                    WHERE id = %s
                """, (
                    name,
                    education,
                    skills,
                    student_id
                ))

                connection.commit()

            finally:
                connection.close()


            return jsonify({
                "success": True,
                "message": "Student profile updated successfully!",
                "student_id": student_id
            }), 200


        # --------------------------------------------------
        # CREATE NEW STUDENT
        # --------------------------------------------------

        student_id = create_student(
            name,
            email,
            education,
            skills,
            ""
        )

        return jsonify({
            "success": True,
            "message": "Student profile created successfully!",
            "student_id": student_id
        }), 201


    except psycopg.errors.UniqueViolation:

        return jsonify({
            "success": False,
            "message": "This email is already registered."
        }), 409


    except Exception as error:

        print(
            "PROFILE CREATION ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "message": (
                "Unable to create student profile. "
                "Please try again."
            )
        }), 500


# ======================================================
# GET STUDENT PROFILE
# ======================================================

@student_bp.route(
    "/api/student/<int:student_id>",
    methods=["GET"]
)
def get_student_profile(student_id):

    student = get_student(student_id)

    if student is None:

        return jsonify({
            "success": False,
            "message": "Student not found."
        }), 404

    return jsonify({
        "success": True,
        "student": {
            "id": student["id"],
            "name": student["name"],
            "email": student["email"],
            "education": student["education"],
            "skills": student["skills"],
            "projects": student["projects"]
        }
    }), 200