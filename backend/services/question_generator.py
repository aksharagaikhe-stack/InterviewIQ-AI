import random


TECHNICAL_QUESTIONS = {
    "beginner": [
        "What is Object-Oriented Programming?",
        "What is the difference between a class and an object?",
        "What is a variable?",
        "What is a function?",
        "What is an array?",
        "What is a database?",
        "What is an API?",
        "What is Git and why is it used?",
        "What is the difference between frontend and backend?",
        "What is HTML?",
        "What is CSS?",
        "What is JavaScript?",
        "What is a loop?",
        "What is conditional statement?",
        "What is exception handling?"
    ],

    "intermediate": [
        "Explain inheritance in Object-Oriented Programming.",
        "What is polymorphism?",
        "What is encapsulation?",
        "What is abstraction?",
        "What is normalization in databases?",
        "What is a REST API?",
        "Explain SQL and NoSQL databases.",
        "What is time complexity?",
        "What is authentication?",
        "What is authorization?",
        "What is the difference between HTTP and HTTPS?",
        "What is a primary key?",
        "What is a foreign key?",
        "What is recursion?",
        "What is the difference between stack and queue?"
    ],

    "advanced": [
        "Explain the SOLID principles.",
        "What are design patterns and why are they useful?",
        "Explain database indexing.",
        "How does caching improve application performance?",
        "Explain the difference between processes and threads.",
        "What is concurrency?",
        "What is a microservice architecture?",
        "Explain load balancing.",
        "What is horizontal scaling?",
        "Explain database transactions and ACID properties."
    ]
}


HR_QUESTIONS = {
    "beginner": [
        "Tell me about yourself.",
        "What are your strengths?",
        "What are your weaknesses?",
        "Why should we hire you?",
        "Why do you want this job?",
        "Where do you see yourself in five years?",
        "Tell me about a project you worked on.",
        "How do you handle pressure?",
        "How do you work in a team?",
        "Why should we select you?",
        "What motivates you?",
        "How do you handle failure?",
        "Tell me about a difficult situation you solved.",
        "What are your career goals?",
        "Why did you choose computer engineering?"
    ],

    "intermediate": [
        "Tell me about a challenging project you completed.",
        "Describe a conflict you faced in a team.",
        "How do you prioritize multiple tasks?",
        "Tell me about a failure and what you learned from it.",
        "How do you handle criticism?",
        "Describe a situation where you showed leadership.",
        "How do you learn a new technology?",
        "Why should we choose you over other candidates?",
        "What type of work environment do you prefer?",
        "How do you deal with deadlines?"
    ]
}


CODING_QUESTIONS = {
    "Python": [
        "Write a Python program to reverse a string.",
        "Write a Python program to find the largest number in a list.",
        "Write a Python program to check whether a number is even or odd.",
        "Write a Python program to calculate factorial of a number.",
        "Write a Python program to count vowels in a string.",
        "Write a Python program to check whether a number is prime.",
        "Write a Python program to find duplicate elements in a list.",
        "Write a Python program to calculate the sum of elements in a list."
    ],

    "Java": [
        "Write a Java program to reverse a string.",
        "Write a Java program to find the largest number in an array.",
        "Write a Java program to check whether a number is prime.",
        "Write a Java program to calculate factorial.",
        "Write a Java program to find the sum of array elements.",
        "Write a Java program to check whether a string is palindrome."
    ],

    "C": [
        "Write a C program to reverse a string.",
        "Write a C program to find the largest number in an array.",
        "Write a C program to check whether a number is prime.",
        "Write a C program to calculate factorial.",
        "Write a C program to find the sum of array elements.",
        "Write a C program to check whether a string is palindrome."
    ],

    "C++": [
        "Write a C++ program to reverse a string.",
        "Write a C++ program to find the largest number in an array.",
        "Write a C++ program to check whether a number is prime.",
        "Write a C++ program to calculate factorial.",
        "Write a C++ program to find the sum of array elements.",
        "Write a C++ program to check whether a string is palindrome."
    ],

    "JavaScript": [
        "Write a JavaScript program to reverse a string.",
        "Write a JavaScript program to find the largest number in an array.",
        "Write a JavaScript program to check whether a number is prime.",
        "Write a JavaScript program to calculate factorial.",
        "Write a JavaScript program to find the sum of array elements.",
        "Write a JavaScript program to check whether a string is palindrome."
    ]
}


def get_question_pool(interview_type, difficulty, language=None):

    difficulty = difficulty.lower()

    if interview_type == "technical":
        return TECHNICAL_QUESTIONS.get(
            difficulty,
            TECHNICAL_QUESTIONS["beginner"]
        )

    if interview_type == "hr":
        return HR_QUESTIONS.get(
            difficulty,
            HR_QUESTIONS["beginner"]
        )

    if interview_type == "coding":
        return CODING_QUESTIONS.get(language, [])

    return []


def generate_questions(
    interview_type,
    difficulty,
    language=None,
    question_count=10
):

    if interview_type == "mixed":

        technical_pool = TECHNICAL_QUESTIONS.get(
            difficulty.lower(),
            TECHNICAL_QUESTIONS["beginner"]
        )

        hr_pool = HR_QUESTIONS.get(
            difficulty.lower(),
            HR_QUESTIONS["beginner"]
        )

        coding_pool = CODING_QUESTIONS.get(
            language,
            []
        )

        combined_pool = (
            technical_pool +
            hr_pool +
            coding_pool
        )

        random.shuffle(combined_pool)

        return [
            combined_pool[i % len(combined_pool)]
            for i in range(question_count)
        ]

    pool = get_question_pool(
        interview_type,
        difficulty,
        language
    )

    if not pool:
        return []

    random.shuffle(pool)

    return [
        pool[i % len(pool)]
        for i in range(question_count)
    ]