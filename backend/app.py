import os

from flask import Flask, send_from_directory
from flask_cors import CORS

from routes.health import health_bp
from routes.student import student_bp
from routes.interview import interview_bp

from models.user import create_users_table
from routes.auth import auth_bp

from models.student import (
    create_table,
    create_interview_history_table,
    add_category_column
)


# ======================================================
# PATHS
# ======================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")


# ======================================================
# CREATE FLASK APP
# ======================================================

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)


# ======================================================
# CORS CONFIGURATION
# ======================================================

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*"
        }
    }
)


# ======================================================
# DATABASE INITIALIZATION
# ======================================================

create_table()
create_interview_history_table()
add_category_column()
create_users_table()


# ======================================================
# REGISTER BLUEPRINTS
# ======================================================

app.register_blueprint(health_bp)
app.register_blueprint(student_bp)
app.register_blueprint(interview_bp)
app.register_blueprint(auth_bp)


# ======================================================
# FRONTEND ROUTES
# ======================================================

@app.route("/")
def home():
    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.route("/<path:filename>")
def frontend_files(filename):
    file_path = os.path.join(FRONTEND_DIR, filename)

    if os.path.isfile(file_path):
        return send_from_directory(
            FRONTEND_DIR,
            filename
        )

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ======================================================
# HEALTH CHECK
# ======================================================

@app.route("/api/status")
def status():

    return {
        "success": True,
        "message": "InterviewIQ AI backend is running",
        "environment": os.getenv(
            "FLASK_ENV",
            "production"
        )
    }


# ======================================================
# RUN SERVER
# ======================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )