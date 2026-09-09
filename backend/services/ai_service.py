import os
import json
from dotenv import load_dotenv
from google import genai

# ============================================================
# GEMINI CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to backend/.env"
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# HELPER FUNCTION
# ============================================================

def clean_json_response(text):
    """
    Cleans Gemini response and converts it into Python JSON.
    """

    if not text:
        raise ValueError("AI returned an empty response.")

    text = text.strip()

    # Remove markdown code fences if Gemini returns them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text.replace("```", "")
        text = text.strip()

    # Sometimes Gemini may return extra text before/after JSON.
    # Try to extract the JSON object.
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return json.loads(text)


# ============================================================
# GENERATE AI INTERVIEW QUESTIONS
# ============================================================

def generate_ai_questions(
    student_profile,
    interview_type,
    role,
    difficulty,
    language,
    question_count,
    category=None
):
    """
    Generate personalized interview questions using Gemini.

    Supported interview types:
        - technical
        - coding
        - hr
        - mixed

    Supported technical categories:
        - Python
        - C
        - C++
        - Java
        - OOP
        - DSA

    HR category:
        - Behavioral

    Coding category:
        - Programming

    Mixed category:
        - Mixed
    """

    # --------------------------------------------------------
    # Default category handling
    # --------------------------------------------------------

    if category is None:
        if interview_type == "technical":
            category = "Technical"
        elif interview_type == "coding":
            category = "Programming"
        elif interview_type == "hr":
            category = "Behavioral"
        elif interview_type == "mixed":
            category = "Mixed"
        else:
            category = "General"

    # --------------------------------------------------------
    # Category-specific instructions
    # --------------------------------------------------------

    category_instruction = ""

    if interview_type == "technical":

        category_instruction = f"""
The selected technical category is: {category}

IMPORTANT:
All questions MUST focus strongly on the selected category.

If category is Python:
- Ask Python programming and Python concept questions.
- Cover topics such as syntax, data types, functions, lists,
  tuples, dictionaries, exceptions, OOP, modules, etc.

If category is C:
- Ask C programming and C concept questions.
- Cover topics such as pointers, arrays, functions, structures,
  memory management, strings, loops, etc.

If category is C++:
- Ask C++ programming and C++ concept questions.
- Cover topics such as classes, objects, inheritance,
  polymorphism, STL, pointers, constructors, etc.

If category is Java:
- Ask Java programming and Java concept questions.
- Cover topics such as classes, objects, inheritance,
  interfaces, exceptions, collections, JVM, etc.

If category is OOP:
- Focus on Object-Oriented Programming concepts.
- Include classes, objects, encapsulation, inheritance,
  polymorphism, abstraction, constructors, interfaces, etc.

If category is DSA:
- Focus on Data Structures and Algorithms.
- Include arrays, linked lists, stacks, queues, trees,
  searching, sorting, recursion, hashing, complexity, etc.
"""

    elif interview_type == "coding":

        category_instruction = """
The interview category is Programming.

Generate programming/coding questions.

Questions should test:
- Problem solving
- Programming logic
- Algorithms
- Data structures
- Code writing
- Debugging
- Time and space complexity where appropriate

The programming language must match the selected language.
"""

    elif interview_type == "hr":

        category_instruction = """
The interview category is Behavioral.

Generate HR/behavioral interview questions.

Focus on:
- Self introduction
- Strengths and weaknesses
- Teamwork
- Leadership
- Conflict handling
- Problem solving
- Career goals
- Motivation
- Adaptability
- Projects and experiences
"""

    elif interview_type == "mixed":

        category_instruction = """
This is a Mixed interview.

Combine:
- Technical questions
- Programming/coding questions
- HR/behavioral questions

The interview should feel like a realistic fresher job interview.

Do not make every question from only one area.
Maintain a reasonable balance between technical,
coding and behavioral questions.
"""

    # --------------------------------------------------------
    # Language instruction
    # --------------------------------------------------------

    language_instruction = ""

    if language:
        language_instruction = f"""
Selected programming language: {language}

When asking programming or coding questions:
- Use {language}.
- Make the question appropriate for the selected language.
- Do not switch to another programming language.
"""

    # --------------------------------------------------------
    # Gemini Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an expert technical and HR interviewer conducting
a realistic job interview for a student/fresher.

Generate exactly {question_count} interview questions.

============================================================
STUDENT PROFILE
============================================================

Name:
{student_profile.get("name", "")}

Education:
{student_profile.get("education", "")}

Skills:
{student_profile.get("skills", "")}

Projects:
{student_profile.get("projects", "")}


============================================================
INTERVIEW DETAILS
============================================================

Interview Type:
{interview_type}

Category:
{category}

Target Role:
{role}

Difficulty:
{difficulty}

Programming Language:
{language}


============================================================
CATEGORY REQUIREMENTS
============================================================

{category_instruction}

{language_instruction}


============================================================
GENERAL REQUIREMENTS
============================================================

1. Questions must match the selected interview type.

2. Questions must match the selected category.

3. Questions must match the selected target role.

4. Questions must match the selected difficulty.

5. Personalize questions using the student's skills and
   projects when relevant.

6. Questions should be suitable for a student/fresher.

7. Avoid extremely advanced questions unless difficulty
   is Hard.

8. Do not ask duplicate or nearly identical questions.

9. Questions should be clear and easy to understand.

10. Do not include answers.

11. Do not include explanations.

12. Do not number the questions inside the question text.

13. For coding interviews, include programming/problem-solving
    questions.

14. For HR interviews, include behavioral questions.

15. For technical interviews, focus on the selected technical
    category.

16. For mixed interviews, combine technical, coding and
    behavioral questions.

17. Make questions realistic for an actual job interview.


============================================================
DIFFICULTY GUIDELINES
============================================================

Easy:
- Basic concepts
- Simple examples
- Fundamental programming questions

Medium:
- Conceptual understanding
- Practical application
- Moderate problem solving

Hard:
- Advanced concepts
- Complex problem solving
- Optimization
- Deeper technical understanding


============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Do not use markdown.

Use exactly this format:

{{
    "questions": [
        "Question 1",
        "Question 2",
        "Question 3"
    ]
}}

The number of questions MUST be exactly {question_count}.
"""

    # --------------------------------------------------------
    # Call Gemini
    # --------------------------------------------------------

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    # --------------------------------------------------------
    # Parse response
    # --------------------------------------------------------

    result = clean_json_response(response.text)

    questions = result.get("questions", [])

    if not isinstance(questions, list):
        raise ValueError("AI returned an invalid questions format.")

    # Keep only non-empty questions
    questions = [
        str(question).strip()
        for question in questions
        if str(question).strip()
    ]

    if not questions:
        raise ValueError("AI did not generate any questions.")

    return questions


# ============================================================
# EVALUATE STUDENT ANSWER
# ============================================================

def evaluate_ai_answer(
    student_profile,
    question,
    answer,
    interview_type,
    role,
    language,
    category=None
):
    """
    Evaluate a student's interview answer using Gemini.
    """

    # --------------------------------------------------------
    # Default category handling
    # --------------------------------------------------------

    if category is None:
        if interview_type == "technical":
            category = "Technical"
        elif interview_type == "coding":
            category = "Programming"
        elif interview_type == "hr":
            category = "Behavioral"
        elif interview_type == "mixed":
            category = "Mixed"
        else:
            category = "General"

    # --------------------------------------------------------
    # Category evaluation instructions
    # --------------------------------------------------------

    category_instruction = ""

    if interview_type == "technical":

        category_instruction = f"""
Selected technical category: {category}

Evaluate technical correctness according to the selected
category.

For example:
- Python → Python concepts and Python correctness
- C → C concepts and C correctness
- C++ → C++ concepts and C++ correctness
- Java → Java concepts and Java correctness
- OOP → Object-oriented programming concepts
- DSA → Data structures, algorithms and complexity
"""

    elif interview_type == "coding":

        category_instruction = f"""
This is a programming/coding interview.

Programming language:
{language}

Evaluate:
- Programming logic
- Algorithm correctness
- Data structure usage
- Code quality
- Time complexity
- Space complexity
- Language-specific correctness
"""

    elif interview_type == "hr":

        category_instruction = """
This is a Behavioral/HR interview.

Technical correctness should have lower importance.

Focus more on:
- Relevance
- Communication
- Clarity
- Confidence
- Professionalism
- Completeness
- Realistic behavioral response
"""

    elif interview_type == "mixed":

        category_instruction = """
This is a Mixed interview.

Evaluate the answer according to the question type.

For technical/coding questions:
- Technical correctness
- Programming knowledge
- Problem solving

For behavioral questions:
- Communication
- Relevance
- Clarity
- Professionalism
"""


    # --------------------------------------------------------
    # Gemini evaluation prompt
    # --------------------------------------------------------

    prompt = f"""
You are an expert interviewer evaluating a student/fresher.

Evaluate the student's answer fairly and constructively.

============================================================
STUDENT PROFILE
============================================================

Name:
{student_profile.get("name", "")}

Education:
{student_profile.get("education", "")}

Skills:
{student_profile.get("skills", "")}

Projects:
{student_profile.get("projects", "")}


============================================================
INTERVIEW DETAILS
============================================================

Interview Type:
{interview_type}

Category:
{category}

Target Role:
{role}

Programming Language:
{language}


============================================================
QUESTION
============================================================

{question}


============================================================
STUDENT ANSWER
============================================================

{answer}


============================================================
CATEGORY-SPECIFIC EVALUATION
============================================================

{category_instruction}


============================================================
EVALUATION CRITERIA
============================================================

Give a score from 0 to 10 for each category.

1. Technical Correctness
   - Is the answer technically correct?
   - Does it demonstrate proper knowledge?

2. Relevance
   - Does the answer directly address the question?

3. Communication
   - Is the answer communicated professionally?
   - Is the explanation understandable?

4. Grammar
   - Is the English grammar reasonably correct?

5. Clarity
   - Is the answer clear, structured and confident?

6. Overall Score
   - Give an overall score from 0 to 10.
   - Consider the question type and category.

IMPORTANT:

For HR questions, do not unfairly reduce the technical score
because the question is behavioral.

For technical questions, technical correctness is important.

For coding questions, correctness of the programming approach
is especially important.


============================================================
FEEDBACK
============================================================

Also provide:

- Short constructive feedback
- Main strengths
- Main weaknesses
- Specific improvement suggestion
- A better example answer

The better answer should be appropriate for a student/fresher
and should not be unnecessarily long.


============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Do not use markdown.

Use exactly this structure:

{{
    "technical_score": 0,
    "relevance_score": 0,
    "communication_score": 0,
    "grammar_score": 0,
    "clarity_score": 0,
    "overall_score": 0,
    "feedback": "",
    "strengths": [],
    "weaknesses": [],
    "suggestion": "",
    "better_answer": ""
}}

All scores must be numbers between 0 and 10.
"""

    # --------------------------------------------------------
    # Call Gemini
    # --------------------------------------------------------

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    # --------------------------------------------------------
    # Parse response
    # --------------------------------------------------------

    result = clean_json_response(response.text)

    # --------------------------------------------------------
    # Validate required fields
    # --------------------------------------------------------

    required_fields = [
        "technical_score",
        "relevance_score",
        "communication_score",
        "grammar_score",
        "clarity_score",
        "overall_score",
        "feedback",
        "strengths",
        "weaknesses",
        "suggestion",
        "better_answer"
    ]

    for field in required_fields:
        if field not in result:
            result[field] = "" if field in [
                "feedback",
                "suggestion",
                "better_answer"
            ] else []

    # --------------------------------------------------------
    # Ensure scores are numeric
    # --------------------------------------------------------

    score_fields = [
        "technical_score",
        "relevance_score",
        "communication_score",
        "grammar_score",
        "clarity_score",
        "overall_score"
    ]

    for field in score_fields:

        try:
            result[field] = float(result[field])
        except (ValueError, TypeError):
            result[field] = 0.0

        # Keep score between 0 and 10
        result[field] = max(0.0, min(10.0, result[field]))

    return result