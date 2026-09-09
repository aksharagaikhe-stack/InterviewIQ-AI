from services.ai_service import generate_ai_questions


student = {
    "name": "Akshara",
    "education": "Computer Engineering",
    "skills": "Python, C++, HTML, CSS",
    "projects": "InterviewIQ AI"
}


questions = generate_ai_questions(
    student_profile=student,
    interview_type="technical",
    role="Software Developer",
    difficulty="Beginner",
    language=None,
    question_count=5
)


print("\nGenerated Questions:\n")

for number, question in enumerate(
    questions,
    start=1
):
    print(f"{number}. {question}")