
from flask import Blueprint, request, jsonify
from models.student import create_student, get_student
import sqlite3

student_bp = Blueprint("student", __name__)


# ======================================================
# CREATE STUDENT PROFILE
# ======================================================

@student_bp.route("/api/student", methods=["POST"])
def create_student_profile():

    data = request.get_json() or {}

    name = data.get("name", "")
    email = data.get("email", "")
    education = data.get("education", "")
    skills = data.get("skills", "")

    # Validate name
    if not name or not name.strip():
        return jsonify({
            "success": False,
            "message": "Name is required."
        }), 400

    # Validate email
    if not email or not email.strip():
        return jsonify({
            "success": False,
            "message": "Email is required."
        }), 400

    name = name.strip()
    email = email.strip()
    education = education.strip()
    skills = skills.strip()

    try:

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

    except sqlite3.IntegrityError:

        return jsonify({
            "success": False,
            "message": "This email is already registered. Please use another email address."
        }), 409

    except Exception as error:

        print("PROFILE CREATION ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Unable to create student profile. Please try again."
        }), 500


# ======================================================
# GET STUDENT PROFILE
# ======================================================

@student_bp.route("/api/student/<int:student_id>", methods=["GET"])
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
    })

