from flask import Blueprint, request, jsonify

import json

from services.ai_service import (
    generate_ai_questions,
    evaluate_ai_answer
)

from services.question_generator import generate_questions
from services.evaluator import evaluate_answer

from models.student import (
    get_student,
    save_interview_history,
    get_interview_history
)


# ======================================================
# BLUEPRINT
# ======================================================

interview_bp = Blueprint("interview", __name__)


# ======================================================
# SUPPORTED OPTIONS
# ======================================================

SUPPORTED_TYPES = [
    "technical",
    "coding",
    "hr",
    "mixed"
]

SUPPORTED_DIFFICULTIES = [
    "Easy",
    "Medium",
    "Hard"
]

SUPPORTED_LANGUAGES = [
    "Python",
    "Java",
    "C",
    "C++",
    "JavaScript"
]


# ======================================================
# TECHNICAL CATEGORIES
# ======================================================

TECHNICAL_CATEGORIES = [
    "Python",
    "C",
    "C++",
    "Java",
    "OOP",
    "DSA"
]


# ======================================================
# HR CATEGORIES
# ======================================================

HR_CATEGORIES = [
    "Behavioral"
]


# ======================================================
# SPECIAL CATEGORIES
# ======================================================

SPECIAL_CATEGORIES = [
    "Programming",
    "Mixed"
]


# ======================================================
# ALL CATEGORIES
# ======================================================

SUPPORTED_CATEGORIES = (
    TECHNICAL_CATEGORIES
    + HR_CATEGORIES
    + SPECIAL_CATEGORIES
)


# ======================================================
# START INTERVIEW
# ======================================================

@interview_bp.route(
    "/api/interview/start",
    methods=["POST"]
)
def start_interview():

    data = request.get_json() or {}

    # ==================================================
    # GET DATA FROM FRONTEND
    # ==================================================

    student_id = data.get("student_id")

    interview_type = data.get(
        "interview_type",
        "technical"
    )

    category = data.get("category")

    language = data.get("language")

    role = data.get(
        "role",
        "Software Developer"
    )

    difficulty = data.get(
        "difficulty",
        "Easy"
    )

    question_count = data.get(
        "question_count",
        10
    )


    # ==================================================
    # VALIDATE INTERVIEW TYPE
    # ==================================================

    if not isinstance(interview_type, str):

        return jsonify({
            "success": False,
            "message": "Interview type must be text."
        }), 400

    interview_type = interview_type.strip().lower()

    if interview_type not in SUPPORTED_TYPES:

        return jsonify({
            "success": False,
            "message": "Invalid interview type."
        }), 400


    # ==================================================
    # VALIDATE DIFFICULTY
    # ==================================================

    if not isinstance(difficulty, str):

        return jsonify({
            "success": False,
            "message": "Difficulty must be text."
        }), 400

    difficulty = difficulty.strip()

    if difficulty not in SUPPORTED_DIFFICULTIES:

        return jsonify({
            "success": False,
            "message":
                "Invalid difficulty level. "
                "Choose Easy, Medium, or Hard."
        }), 400


    # ==================================================
    # VALIDATE ROLE
    # ==================================================

    if not isinstance(role, str) or not role.strip():

        return jsonify({
            "success": False,
            "message": "Role is required."
        }), 400

    role = role.strip()


    # ==================================================
    # VALIDATE CATEGORY
    # ==================================================

    if interview_type == "technical":

        if not category:

            return jsonify({
                "success": False,
                "message":
                    "Please select a technical category."
            }), 400

        if not isinstance(category, str):

            return jsonify({
                "success": False,
                "message":
                    "Category must be text."
            }), 400

        category = category.strip()

        if category not in TECHNICAL_CATEGORIES:

            return jsonify({
                "success": False,
                "message":
                    "Invalid technical category."
            }), 400


    elif interview_type == "hr":

        if not category:

            category = "Behavioral"

        if not isinstance(category, str):

            return jsonify({
                "success": False,
                "message":
                    "Category must be text."
            }), 400

        category = category.strip()

        if category not in HR_CATEGORIES:

            return jsonify({
                "success": False,
                "message":
                    "Invalid HR category."
            }), 400


    elif interview_type == "coding":

        category = "Programming"


    elif interview_type == "mixed":

        category = "Mixed"


    # ==================================================
    # VALIDATE PROGRAMMING LANGUAGE
    # ==================================================

    if interview_type in [
        "coding",
        "mixed"
    ]:

        if not language:

            return jsonify({
                "success": False,
                "message":
                    "Please select a programming language."
            }), 400

        if not isinstance(language, str):

            return jsonify({
                "success": False,
                "message":
                    "Programming language must be text."
            }), 400

        language = language.strip()

        if language not in SUPPORTED_LANGUAGES:

            return jsonify({
                "success": False,
                "message":
                    "Please select a valid programming language."
            }), 400


    # ==================================================
    # TECHNICAL / HR DON'T REQUIRE LANGUAGE
    # ==================================================

    if interview_type in [
        "technical",
        "hr"
    ]:

        language = None


    # ==================================================
    # VALIDATE QUESTION COUNT
    # ==================================================

    try:

        question_count = int(question_count)

    except (ValueError, TypeError):

        return jsonify({
            "success": False,
            "message":
                "Question count must be a number."
        }), 400


    if question_count < 1 or question_count > 20:

        return jsonify({
            "success": False,
            "message":
                "Question count must be between 1 and 20."
        }), 400


    # ==================================================
    # GET STUDENT PROFILE
    # ==================================================

    student_profile = {
        "name": "",
        "education": "",
        "skills": "",
        "projects": ""
    }


    if student_id:

        try:

            student = get_student(
                int(student_id)
            )

            if student:

                student_profile = {

                    "name":
                        student["name"],

                    "education":
                        student["education"] or "",

                    "skills":
                        student["skills"] or "",

                    "projects":
                        student["projects"] or ""
                }

            else:

                return jsonify({
                    "success": False,
                    "message":
                        "Student not found."
                }), 404


        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "message":
                    "Invalid student ID."
            }), 400


    # ==================================================
    # GENERATE AI QUESTIONS
    # ==================================================

    try:

        questions = generate_ai_questions(

            student_profile=student_profile,

            interview_type=interview_type,

            role=role,

            difficulty=difficulty,

            language=language,

            question_count=question_count,

            category=category
        )


    except Exception as error:

        print(
            "AI Question Generation Error:"
        )

        print(error)

        # ==================================================
        # FALLBACK TO RULE-BASED QUESTIONS
        # ==================================================

        try:

            questions = generate_questions(

                interview_type=interview_type,

                difficulty=difficulty,

                language=language,

                question_count=question_count
            )

        except Exception as fallback_error:

            print(
                "Fallback Question Generation Error:"
            )

            print(fallback_error)

            return jsonify({

                "success":
                    False,

                "message":
                    "Unable to generate interview questions."
            }), 500


    # ==================================================
    # CHECK QUESTIONS
    # ==================================================

    if not questions:

        return jsonify({

            "success":
                False,

            "message":
                "No questions were generated."
        }), 500


    # ==================================================
    # CREATE INTERVIEW SESSION
    # ==================================================

    interview = {

        "student_id":
            student_id,

        "student_profile":
            student_profile,

        "interview_type":
            interview_type,

        "category":
            category,

        "language":
            language,

        "role":
            role,

        "difficulty":
            difficulty,

        "question_count":
            len(questions),

        "question_number":
            1,

        "status":
            "started",

        "questions":
            questions,

        "answers":
            []
    }


    # ==================================================
    # RETURN RESPONSE
    # ==================================================

    return jsonify({

        "success":
            True,

        "message":
            "AI interview started successfully!",

        "interview":
            interview

    }), 201


# ======================================================
# EVALUATE ANSWER
# ======================================================

@interview_bp.route(
    "/api/interview/evaluate",
    methods=["POST"]
)
def evaluate():

    data = request.get_json() or {}


    # ==================================================
    # GET DATA
    # ==================================================

    question = data.get(
        "question",
        ""
    )

    answer = data.get(
        "answer",
        ""
    )

    interview_type = data.get(
        "interview_type",
        "technical"
    )

    category = data.get(
        "category"
    )

    role = data.get(
        "role",
        "Software Developer"
    )

    language = data.get(
        "language"
    )

    student_id = data.get(
        "student_id"
    )


    # ==================================================
    # VALIDATE QUESTION
    # ==================================================

    if not isinstance(question, str) or not question.strip():

        return jsonify({
            "success": False,
            "message":
                "Question is required."
        }), 400

    question = question.strip()


    # ==================================================
    # VALIDATE ANSWER
    # ==================================================

    if not isinstance(answer, str) or not answer.strip():

        return jsonify({
            "success": False,
            "message":
                "Answer is required."
        }), 400

    answer = answer.strip()


    # ==================================================
    # VALIDATE INTERVIEW TYPE
    # ==================================================

    if not isinstance(interview_type, str):

        return jsonify({
            "success": False,
            "message":
                "Interview type must be text."
        }), 400

    interview_type = interview_type.strip().lower()

    if interview_type not in SUPPORTED_TYPES:

        return jsonify({
            "success": False,
            "message":
                "Invalid interview type."
        }), 400


    # ==================================================
    # VALIDATE ROLE
    # ==================================================

    if not isinstance(role, str) or not role.strip():

        return jsonify({
            "success": False,
            "message":
                "Role is required."
        }), 400

    role = role.strip()


    # ==================================================
    # NORMALIZE CATEGORY
    # ==================================================

    if interview_type == "technical":

        if not category:

            return jsonify({
                "success": False,
                "message":
                    "Technical category is required."
            }), 400

        if not isinstance(category, str):

            return jsonify({
                "success": False,
                "message":
                    "Category must be text."
            }), 400

        category = category.strip()

        if category not in TECHNICAL_CATEGORIES:

            return jsonify({
                "success": False,
                "message":
                    "Invalid technical category."
            }), 400


    elif interview_type == "hr":

        if not category:

            category = "Behavioral"

        if category not in HR_CATEGORIES:

            return jsonify({
                "success": False,
                "message":
                    "Invalid HR category."
            }), 400


    elif interview_type == "coding":

        category = "Programming"


    elif interview_type == "mixed":

        category = "Mixed"


    # ==================================================
    # VALIDATE LANGUAGE
    # ==================================================

    if interview_type in [
        "coding",
        "mixed"
    ]:

        if not language:

            return jsonify({
                "success": False,
                "message":
                    "Programming language is required."
            }), 400

        if not isinstance(language, str):

            return jsonify({
                "success": False,
                "message":
                    "Programming language must be text."
            }), 400

        language = language.strip()

        if language not in SUPPORTED_LANGUAGES:

            return jsonify({
                "success": False,
                "message":
                    "Invalid programming language."
            }), 400

    else:

        language = None


    # ==================================================
    # GET STUDENT PROFILE
    # ==================================================

    student_profile = {

        "name": "",

        "education": "",

        "skills": "",

        "projects": ""
    }


    if student_id:

        try:

            student = get_student(
                int(student_id)
            )

            if student:

                student_profile = {

                    "name":
                        student["name"],

                    "education":
                        student["education"] or "",

                    "skills":
                        student["skills"] or "",

                    "projects":
                        student["projects"] or ""
                }

            else:

                return jsonify({

                    "success":
                        False,

                    "message":
                        "Student not found."
                }), 404


        except (ValueError, TypeError):

            return jsonify({

                "success":
                    False,

                "message":
                    "Invalid student ID."
            }), 400


    # ==================================================
    # REAL AI EVALUATION
    # ==================================================

    try:

        evaluation = evaluate_ai_answer(

            student_profile=student_profile,

            question=question,

            answer=answer,

            interview_type=interview_type,

            role=role,

            language=language,

            category=category
        )


        return jsonify({

            "success":
                True,

            "evaluation":
                evaluation,

            "source":
                "gemini-ai"

        }), 200


    except Exception as error:

        print(
            "AI Evaluation Error:"
        )

        print(error)


        # ==================================================
        # FALLBACK EVALUATION
        # ==================================================

        try:

            evaluation = evaluate_answer(

                question=question,

                answer=answer,

                interview_type=interview_type
            )


            return jsonify({

                "success":
                    True,

                "evaluation":
                    evaluation,

                "source":
                    "rule-based-fallback"

            }), 200


        except Exception as fallback_error:

            print(
                "Fallback Evaluation Error:"
            )

            print(fallback_error)


            return jsonify({

                "success":
                    False,

                "message":
                    "Unable to evaluate the answer."

            }), 500


# ======================================================
# SAVE INTERVIEW HISTORY
# ======================================================

@interview_bp.route(
    "/api/interview/history",
    methods=["POST"]
)
def save_history():

    data = request.get_json() or {}


    # ==================================================
    # GET DATA
    # ==================================================

    student_id = data.get(
        "student_id"
    )

    interview_type = data.get(
        "interview_type",
        "technical"
    )

    category = data.get(
        "category"
    )

    role = data.get(
        "role",
        "Software Developer"
    )

    difficulty = data.get(
        "difficulty",
        "Easy"
    )

    language = data.get(
        "language"
    )

    question_count = data.get(
        "question_count",
        0
    )

    overall_score = data.get(
        "overall_score",
        0
    )

    technical_score = data.get(
        "technical_score",
        0
    )

    communication_score = data.get(
        "communication_score",
        0
    )

    relevance_score = data.get(
        "relevance_score",
        0
    )

    grammar_score = data.get(
        "grammar_score",
        0
    )

    clarity_score = data.get(
        "clarity_score",
        0
    )

    strengths = data.get(
        "strengths",
        []
    )

    weaknesses = data.get(
        "weaknesses",
        []
    )

    suggestions = data.get(
        "suggestions",
        []
    )


    # ==================================================
    # VALIDATE STUDENT
    # ==================================================

    if not student_id:

        return jsonify({

            "success":
                False,

            "message":
                "Student ID is required."
        }), 400


    # ==================================================
    # VALIDATE INTERVIEW TYPE
    # ==================================================

    if not isinstance(interview_type, str):

        return jsonify({

            "success":
                False,

            "message":
                "Interview type must be text."
        }), 400

    interview_type = interview_type.strip().lower()

    if interview_type not in SUPPORTED_TYPES:

        return jsonify({

            "success":
                False,

            "message":
                "Invalid interview type."
        }), 400


    # ==================================================
    # NORMALIZE CATEGORY
    # ==================================================

    if interview_type == "technical":

        if not category:

            return jsonify({

                "success":
                    False,

                "message":
                    "Technical category is required."
            }), 400

        if not isinstance(category, str):

            return jsonify({

                "success":
                    False,

                "message":
                    "Category must be text."
            }), 400

        category = category.strip()

        if category not in TECHNICAL_CATEGORIES:

            return jsonify({

                "success":
                    False,

                "message":
                    "Invalid technical category."
            }), 400


    elif interview_type == "hr":

        category = category or "Behavioral"

        if category not in HR_CATEGORIES:

            return jsonify({

                "success":
                    False,

                "message":
                    "Invalid HR category."
            }), 400


    elif interview_type == "coding":

        category = "Programming"


    elif interview_type == "mixed":

        category = "Mixed"


    # ==================================================
    # VALIDATE DIFFICULTY
    # ==================================================

    if not isinstance(difficulty, str):

        return jsonify({

            "success":
                False,

            "message":
                "Difficulty must be text."
        }), 400

    difficulty = difficulty.strip()

    if difficulty not in SUPPORTED_DIFFICULTIES:

        return jsonify({

            "success":
                False,

            "message":
                "Invalid difficulty level."
        }), 400


    # ==================================================
    # VALIDATE QUESTION COUNT
    # ==================================================

    try:

        question_count = int(
            question_count
        )

    except (ValueError, TypeError):

        return jsonify({

            "success":
                False,

            "message":
                "Question count must be a number."
        }), 400


    if question_count < 1 or question_count > 20:

        return jsonify({

            "success":
                False,

            "message":
                "Question count must be between 1 and 20."
        }), 400


    # ==================================================
    # CHECK STUDENT EXISTS
    # ==================================================

    try:

        student = get_student(
            int(student_id)
        )

    except (ValueError, TypeError):

        return jsonify({

            "success":
                False,

            "message":
                "Invalid student ID."
        }), 400


    if student is None:

        return jsonify({

            "success":
                False,

            "message":
                "Student not found."
        }), 404


    # ==================================================
    # SAVE HISTORY
    # ==================================================

    try:

        history_id = save_interview_history(

            student_id=int(
                student_id
            ),

            interview_type=
                interview_type,

            category=
                category,

            role=
                role,

            difficulty=
                difficulty,

            language=
                language,

            question_count=
                question_count,

            overall_score=
                overall_score,

            technical_score=
                technical_score,

            communication_score=
                communication_score,

            relevance_score=
                relevance_score,

            grammar_score=
                grammar_score,

            clarity_score=
                clarity_score,

            strengths=
                json.dumps(
                    strengths
                ),

            weaknesses=
                json.dumps(
                    weaknesses
                ),

            suggestions=
                json.dumps(
                    suggestions
                )
        )


        return jsonify({

            "success":
                True,

            "message":
                "Interview history saved successfully.",

            "history_id":
                history_id

        }), 201


    except Exception as error:

        print(
            "Save Interview History Error:"
        )

        print(error)


        return jsonify({

            "success":
                False,

            "message":
                "Unable to save interview history. "
                "Please try again."

        }), 500


# ======================================================
# GET INTERVIEW HISTORY
# ======================================================

@interview_bp.route(
    "/api/interview/history/<int:student_id>",
    methods=["GET"]
)
def history(student_id):

    # ==================================================
    # CHECK STUDENT
    # ==================================================

    student = get_student(
        student_id
    )


    if student is None:

        return jsonify({

            "success":
                False,

            "message":
                "Student not found."

        }), 404


    # ==================================================
    # GET HISTORY
    # ==================================================

    try:

        history_data = get_interview_history(
            student_id
        )


        history_list = []


        for item in history_data:

            history_list.append({

                "id":
                    item["id"],

                "student_id":
                    item["student_id"],

                "interview_type":
                    item["interview_type"],

                "category":
                    item["category"],

                "role":
                    item["role"],

                "difficulty":
                    item["difficulty"],

                "language":
                    item["language"],

                "question_count":
                    item["question_count"],

                "overall_score":
                    item["overall_score"],

                "technical_score":
                    item["technical_score"],

                "communication_score":
                    item["communication_score"],

                "relevance_score":
                    item["relevance_score"],

                "grammar_score":
                    item["grammar_score"],

                "clarity_score":
                    item["clarity_score"],

                "strengths":
                    json.loads(
                        item["strengths"] or "[]"
                    ),

                "weaknesses":
                    json.loads(
                        item["weaknesses"] or "[]"
                    ),

                "suggestions":
                    json.loads(
                        item["suggestions"] or "[]"
                    ),

                "created_at":
                    item["created_at"]
            })


        return jsonify({

            "success":
                True,

            "student": {

                "id":
                    student["id"],

                "name":
                    student["name"]

            },

            "history":
                history_list

        }), 200


    except Exception as error:

        print(
            "Get Interview History Error:"
        )

        print(error)


        return jsonify({

            "success":
                False,

            "message":
                "Unable to retrieve interview history. "
                "Please try again."

        }), 500