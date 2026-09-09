def evaluate_answer(
    question,
    answer,
    interview_type
):

    if not answer or not answer.strip():

        return {
            "score": 0,
            "technical_score": 0,
            "communication_score": 0,
            "relevance_score": 0,
            "feedback": "No answer was provided.",
            "suggestion": "Try to answer the question instead of leaving it blank."
        }


    answer = answer.strip()

    words = answer.split()
    word_count = len(words)


    # Basic communication score
    if word_count >= 50:
        communication_score = 10
    elif word_count >= 30:
        communication_score = 8
    elif word_count >= 15:
        communication_score = 6
    elif word_count >= 5:
        communication_score = 4
    else:
        communication_score = 2


    # Basic relevance score
    question_words = set(
        question.lower().replace("?", "").split()
    )

    answer_words = set(
        answer.lower().split()
    )

    common_words = question_words.intersection(
        answer_words
    )

    if len(common_words) >= 3:
        relevance_score = 9
    elif len(common_words) >= 2:
        relevance_score = 7
    elif len(common_words) >= 1:
        relevance_score = 5
    else:
        relevance_score = 3


    # Basic technical score
    if interview_type == "hr":

        technical_score = 8

    elif interview_type == "coding":

        if word_count >= 20:
            technical_score = 8
        elif word_count >= 10:
            technical_score = 6
        else:
            technical_score = 3

    else:

        if word_count >= 40:
            technical_score = 8
        elif word_count >= 20:
            technical_score = 6
        elif word_count >= 8:
            technical_score = 4
        else:
            technical_score = 2


    total_score = round(
        (
            technical_score +
            communication_score +
            relevance_score
        ) / 3,
        1
    )


    if total_score >= 8:
        feedback = "Excellent answer. Your response was clear and relevant."

    elif total_score >= 6:
        feedback = "Good answer. You can improve it by adding more explanation and examples."

    elif total_score >= 4:
        feedback = "Average answer. Try to explain your concept more clearly."

    else:
        feedback = "Your answer needs improvement. Provide a more detailed and relevant response."


    suggestion = (
        "Use a structured answer, explain the main concept, "
        "and include an example wherever possible."
    )


    return {
        "score": total_score,
        "technical_score": technical_score,
        "communication_score": communication_score,
        "relevance_score": relevance_score,
        "feedback": feedback,
        "suggestion": suggestion
    }