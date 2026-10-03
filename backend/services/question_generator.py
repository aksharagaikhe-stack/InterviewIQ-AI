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
        "What is exception handling?",
            "What is an algorithm?",
      "What is Big-O notation?",
      "What is a database?",
      "What is an API?",
      "What is HTTP?",
      "What is JSON?",
      "What is Git?",
      "What is a process?",
      "What is a thread?",
      "What is debugging?",
      "What is authentication?",
      "What is authorization?",
      "What is caching?",
      "What is a server?",
      "What is cloud computing?",
      "What is a primary key?",
      "What is a foreign key?",
      "What is an IP address?",
      "What is DNS?",
      "What is a firewall?",
      "What is Docker?",
      "What is CI/CD?",
      "What is a microservice?",
      "What is a load balancer?",
      "What is a message queue?"
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
        "What is the difference between stack and queue?","Explain the difference between a process and a thread.",
      "What is the difference between TCP and UDP?",
      "Explain how DNS works.",
      "What happens when you enter a URL into a browser?",
      "Explain HTTP status codes such as 200, 301, 400, 401, 403, 404, and 500.",
      "What is the difference between HTTP and HTTPS?",
      "Explain REST API and its main principles.",
      "What is the difference between GET, POST, PUT, PATCH, and DELETE?",
      "Explain authentication vs authorization.",
      "What is JWT and how does it work?",
      "What is database normalization?",
      "Explain SQL vs NoSQL databases.",
      "What is database indexing and why does it improve performance?",
      "What is a database transaction?",
      "Explain ACID properties.",
      "What is a deadlock?",
      "What is a race condition?",
      "What is multithreading?",
      "What is concurrency vs parallelism?",
      "What is caching and where can caching be implemented?",
      "What is load balancing?",
      "Explain horizontal vs vertical scaling.",
      "What is a message queue?",
      "What is Docker and why is it used?",
      "What is CI/CD?",
      "What is a microservice?",
      "What is a reverse proxy?",
      "What is a CDN?",
      "How would you troubleshoot a slow API?",
      "How would you troubleshoot an application that suddenly crashes?"
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
        "Explain database transactions and ACID properties.","Explain everything that happens from entering a URL in a browser until the webpage is displayed.",
      "Design a scalable backend capable of handling millions of requests.",
      "How would you design a highly available web application?",
      "Explain how load balancing, caching, database replication, and message queues work together.",
      "Design a distributed caching system.",
      "Design a rate-limiting system for an API.",
      "Design a scalable authentication and authorization system.",
      "Design a real-time chat application.",
      "Design a payment-processing system.",
      "Design a notification system supporting email, SMS, and push notifications.",
      "Design a URL-shortening service.",
      "Design a file-storage system similar to cloud storage.",
      "Design a video-streaming platform.",
      "Design a scalable social-media feed.",
      "Design a distributed job-processing system.",
      "How would you design a system that supports millions of concurrent users?",
      "Explain database sharding and when it should be used.",
      "Explain database replication and read replicas.",
      "How would you migrate a huge production database with minimal downtime?",
      "How would you diagnose a production system with high CPU usage?",
      "How would you diagnose a production system with continuously increasing memory usage?",
      "How would you investigate intermittent API failures?",
      "How would you troubleshoot high network latency?",
      "How would you identify and fix a race condition in production?",
      "How would you diagnose a database deadlock?",
      "Explain eventual consistency and when it is acceptable.",
      "Explain CAP theorem with a practical example.",
      "Explain fault tolerance and disaster recovery.",
      "How would you design a system with zero-downtime deployment?",
      "How would you design monitoring and alerting for a production system?"
      
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