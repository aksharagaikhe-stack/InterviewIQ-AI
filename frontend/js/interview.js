// ======================================================
// InterviewIQ AI
// AI Mock Interview JavaScript
// ======================================================

let interviewData = null;

let currentQuestionIndex = 0;

let answers = [];


// ======================================================
// DOM ELEMENTS
// ======================================================

const questionText =
    document.getElementById(
        "questionText"
    );

const questionProgress =
    document.getElementById(
        "questionProgress"
    );

const answer =
    document.getElementById(
        "answer"
    );

const wordCount =
    document.getElementById(
        "wordCount"
    );

const submitAnswerBtn =
    document.getElementById(
        "submitAnswerBtn"
    );

const nextQuestionBtn =
    document.getElementById(
        "nextQuestionBtn"
    );

const finishBtn =
    document.getElementById(
        "finishBtn"
    );

const evaluationBox =
    document.getElementById(
        "evaluationBox"
    );

const statusMessage =
    document.getElementById(
        "statusMessage"
    );

const feedbackText =
    document.getElementById(
        "feedbackText"
    );

const suggestionText =
    document.getElementById(
        "suggestionText"
    );

const scoreText =
    document.getElementById(
        "scoreText"
    );

const technicalScore =
    document.getElementById(
        "technicalScore"
    );

const communicationScore =
    document.getElementById(
        "communicationScore"
    );


// ======================================================
// LOAD INTERVIEW
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const storedInterview =
            localStorage.getItem(
                "interview_data"
            );


        if (!storedInterview) {

            alert(
                "Interview session not found. Please start an interview first."
            );

            window.location.href =
                "interview-selection.html";

            return;

        }


        try {

            interviewData =
                JSON.parse(
                    storedInterview
                );


            if (
                !interviewData.questions ||
                !Array.isArray(
                    interviewData.questions
                ) ||
                interviewData.questions.length === 0
            ) {

                throw new Error(
                    "No interview questions found."
                );

            }


            loadInterviewInfo();

            loadQuestion();


        } catch (error) {

            console.error(
                "Interview Data Error:",
                error
            );


            alert(
                "Invalid interview session. Please start again."
            );


            localStorage.removeItem(
                "interview_data"
            );


            window.location.href =
                "interview-selection.html";

        }

    }
);


// ======================================================
// INTERVIEW INFORMATION
// ======================================================

function loadInterviewInfo() {

    const element =
        document.getElementById(
            "interviewInfo"
        );


    if (!element) {
        return;
    }


    let info =
        `${interviewData.role || "Software Developer"} • ` +
        `${interviewData.difficulty || "Medium"} • ` +
        `${formatInterviewType(
            interviewData.interview_type
        )}`;


    if (interviewData.category) {

        info +=
            ` • ${interviewData.category}`;

    }


    if (interviewData.language) {

        info +=
            ` • ${interviewData.language}`;

    }


    element.textContent =
        info;

}


// ======================================================
// FORMAT INTERVIEW TYPE
// ======================================================

function formatInterviewType(type) {

    const map = {

        technical:
            "Technical Interview",

        coding:
            "Coding Interview",

        hr:
            "HR Interview",

        mixed:
            "Mixed Interview"

    };


    return (
        map[type] ||
        "Interview"
    );

}


// ======================================================
// LOAD QUESTION
// ======================================================

function loadQuestion() {

    const questions =
        interviewData.questions;


    if (
        !questions ||
        questions.length === 0
    ) {

        questionText.textContent =
            "No questions available.";

        return;

    }


    const question =
        questions[
            currentQuestionIndex
        ];


    // ==============================================
    // QUESTION
    // ==============================================

    questionText.textContent =
        question;


    // ==============================================
    // PROGRESS
    // ==============================================

    questionProgress.textContent =
        `Question ${
            currentQuestionIndex + 1
        } of ${
            questions.length
        }`;


    // ==============================================
    // RESET ANSWER
    // ==============================================

    answer.value = "";

    updateWordCount();


    // ==============================================
    // RESET EVALUATION
    // ==============================================

    evaluationBox.style.display =
        "none";


    submitAnswerBtn.style.display =
        "inline-block";

    submitAnswerBtn.disabled =
        false;


    nextQuestionBtn.style.display =
        "none";


    finishBtn.style.display =
        "none";


    statusMessage.textContent =
        "";


    answer.focus();

}


// ======================================================
// WORD COUNT
// ======================================================

function updateWordCount() {

    if (!answer || !wordCount) {
        return;
    }


    const text =
        answer.value.trim();


    if (!text) {

        wordCount.textContent =
            "0 words";

        return;

    }


    const words =
        text.split(/\s+/);


    wordCount.textContent =
        `${words.length} words`;

}


if (answer) {

    answer.addEventListener(
        "input",
        updateWordCount
    );

}


// ======================================================
// SUBMIT ANSWER
// ======================================================

if (submitAnswerBtn) {

    submitAnswerBtn.addEventListener(
        "click",
        submitAnswer
    );

}


async function submitAnswer() {

    const studentAnswer =
        answer.value.trim();


    // ==============================================
    // VALIDATE
    // ==============================================

    if (!studentAnswer) {

        statusMessage.textContent =
            "Please enter an answer.";

        answer.focus();

        return;

    }


    if (
        studentAnswer.length < 2
    ) {

        statusMessage.textContent =
            "Please provide a more complete answer.";

        return;

    }


    // ==============================================
    // DISABLE BUTTON
    // ==============================================

    submitAnswerBtn.disabled =
        true;


    statusMessage.textContent =
        "AI is evaluating your answer...";


    const question =
        interviewData.questions[
            currentQuestionIndex
        ];


    // ==============================================
    // REQUEST
    // ==============================================

    const requestData = {

        student_id:
            Number(
                interviewData.student_id
            ),

        question:
            question,

        answer:
            studentAnswer,

        interview_type:
            interviewData.interview_type,

        category:
            interviewData.category,

        role:
            interviewData.role,

        language:
            interviewData.language

    };


    try {

        const response =
            await fetch(
                `${API_URL}/api/interview/evaluate`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            requestData
                        )
                }
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.message ||
                "Evaluation failed."
            );

        }


        const evaluation =
            data.evaluation;


        if (!evaluation) {

            throw new Error(
                "No evaluation was returned."
            );

        }


        // ==========================================
        // SAVE ANSWER
        // ==========================================

        answers.push({

            question:
                question,

            answer:
                studentAnswer,

            evaluation:
                evaluation

        });


        // ==========================================
        // SHOW EVALUATION
        // ==========================================

        showEvaluation(
            evaluation
        );


        submitAnswerBtn.style.display =
            "none";


        // ==========================================
        // NEXT / FINISH
        // ==========================================

        if (
            currentQuestionIndex <
            interviewData.questions.length - 1
        ) {

            nextQuestionBtn.style.display =
                "inline-block";

        } else {

            finishBtn.style.display =
                "inline-block";

        }


        statusMessage.textContent =
            data.source === "gemini-ai"
                ? "AI evaluation completed successfully."
                : "Evaluation completed.";


    } catch (error) {

        console.error(
            "Evaluation Error:",
            error
        );


        statusMessage.textContent =
            error.message ||
            "Unable to evaluate answer. Please try again.";


        submitAnswerBtn.disabled =
            false;

    }

}


// ======================================================
// SHOW EVALUATION
// ======================================================

function showEvaluation(
    evaluation
) {

    evaluationBox.style.display =
        "block";


    if (feedbackText) {

        feedbackText.textContent =
            evaluation.feedback ||
            "No feedback available.";

    }


    if (suggestionText) {

        suggestionText.textContent =
            `Suggestion: ${
                evaluation.suggestion ||
                "Keep practicing your answers."
            }`;

    }


    if (scoreText) {

        scoreText.textContent =
            Number(
                evaluation.overall_score ??
                evaluation.score ??
                0
            ).toFixed(1);

    }


    if (technicalScore) {

        technicalScore.textContent =
            Number(
                evaluation.technical_score ??
                0
            ).toFixed(1);

    }


    if (communicationScore) {

        communicationScore.textContent =
            Number(
                evaluation.communication_score ??
                0
            ).toFixed(1);

    }

}


// ======================================================
// NEXT QUESTION
// ======================================================

if (nextQuestionBtn) {

    nextQuestionBtn.addEventListener(
        "click",
        function () {

            currentQuestionIndex++;


            if (
                currentQuestionIndex >=
                interviewData.questions.length
            ) {

                finishInterview();

                return;

            }


            loadQuestion();

        }
    );

}


// ======================================================
// FINISH BUTTON
// ======================================================

if (finishBtn) {

    finishBtn.addEventListener(
        "click",
        finishInterview
    );

}


// ======================================================
// FINISH INTERVIEW
// ======================================================

function finishInterview() {

    if (
        !interviewData ||
        !interviewData.questions
    ) {

        return;

    }


    const totalQuestions =
        interviewData.questions.length;


    const answeredQuestions =
        answers.length;


    if (answeredQuestions === 0) {

        alert(
            "Please answer at least one question before finishing."
        );

        return;

    }


    let totalScore = 0;

    let totalTechnical = 0;

    let totalCommunication = 0;

    let totalRelevance = 0;

    let totalGrammar = 0;

    let totalClarity = 0;


    let allFeedback = [];

    let allStrengths = [];

    let allWeaknesses = [];

    let allSuggestions = [];


    // ==============================================
    // PROCESS ANSWERS
    // ==============================================

    answers.forEach(function (item) {

        const evaluation =
            item.evaluation || {};


        totalScore += Number(
            evaluation.overall_score ??
            evaluation.score ??
            0
        );


        totalTechnical += Number(
            evaluation.technical_score ??
            0
        );


        totalCommunication += Number(
            evaluation.communication_score ??
            0
        );


        totalRelevance += Number(
            evaluation.relevance_score ??
            0
        );


        totalGrammar += Number(
            evaluation.grammar_score ??
            0
        );


        totalClarity += Number(
            evaluation.clarity_score ??
            0
        );


        if (
            evaluation.feedback
        ) {

            allFeedback.push(
                String(
                    evaluation.feedback
                )
            );

        }


        addToArray(
            allStrengths,
            evaluation.strengths
        );


        addToArray(
            allWeaknesses,
            evaluation.weaknesses
        );


        if (
            evaluation.suggestion
        ) {

            allSuggestions.push(
                String(
                    evaluation.suggestion
                )
            );

        }

    });


    // ==============================================
    // AVERAGES
    // ==============================================

    const overallScore =
        average(
            totalScore,
            answeredQuestions
        );


    const technicalAverage =
        average(
            totalTechnical,
            answeredQuestions
        );


    const communicationAverage =
        average(
            totalCommunication,
            answeredQuestions
        );


    const relevanceAverage =
        average(
            totalRelevance,
            answeredQuestions
        );


    const grammarAverage =
        average(
            totalGrammar,
            answeredQuestions
        );


    const clarityAverage =
        average(
            totalClarity,
            answeredQuestions
        );


    // ==============================================
    // REMOVE DUPLICATES
    // ==============================================

    allFeedback =
        uniqueStrings(
            allFeedback
        );


    allStrengths =
        uniqueStrings(
            allStrengths
        );


    allWeaknesses =
        uniqueStrings(
            allWeaknesses
        );


    allSuggestions =
        uniqueStrings(
            allSuggestions
        );


    // ==============================================
    // DEFAULT VALUES
    // ==============================================

    if (allFeedback.length === 0) {

        allFeedback.push(
            "Your AI interview has been completed."
        );

    }


    if (allStrengths.length === 0) {

        allStrengths.push(
            "You completed the interview successfully."
        );

    }


    if (allWeaknesses.length === 0) {

        allWeaknesses.push(
            "Continue practicing to identify further improvement areas."
        );

    }


    if (allSuggestions.length === 0) {

        allSuggestions.push(
            "Continue practicing regularly to improve your interview performance."
        );

    }


    // ==============================================
    // FINAL REPORT
    // ==============================================

    const report = {

        student_id:
            interviewData.student_id,

        student_profile:
            interviewData.student_profile ||
            null,

        interview_type:
            interviewData.interview_type,

        category:
            interviewData.category ||
            null,

        language:
            interviewData.language ||
            null,

        role:
            interviewData.role,

        difficulty:
            interviewData.difficulty,

        total_questions:
            totalQuestions,

        answered_questions:
            answeredQuestions,

        overall_score:
            overallScore,

        technical_score:
            technicalAverage,

        communication_score:
            communicationAverage,

        relevance_score:
            relevanceAverage,

        grammar_score:
            grammarAverage,

        clarity_score:
            clarityAverage,

        feedback:
            allFeedback.join(" "),

        strengths:
            allStrengths,

        weaknesses:
            allWeaknesses,

        suggestions:
            allSuggestions,

        suggestion:
            allSuggestions[0] || "",

        answers:
            answers,

        completed_at:
            new Date().toISOString()

    };


    // ==============================================
    // SAVE
    // ==============================================

    localStorage.setItem(
        "interview_report",
        JSON.stringify(report)
    );


    console.log(
        "Final Interview Report:",
        report
    );


    // ==============================================
    // GO TO REPORT
    // ==============================================

    window.location.href =
        "report.html";

}


// ======================================================
// HELPER: AVERAGE
// ======================================================

function average(
    total,
    count
) {

    if (!count) {
        return 0;
    }


    return Number(
        (
            total / count
        ).toFixed(1)
    );

}


// ======================================================
// HELPER: ARRAY
// ======================================================

function addToArray(
    target,
    value
) {

    if (Array.isArray(value)) {

        value.forEach(function (item) {

            if (item) {

                target.push(
                    String(item)
                );

            }

        });

    }

    else if (value) {

        target.push(
            String(value)
        );

    }

}


// ======================================================
// HELPER: UNIQUE STRINGS
// ======================================================

function uniqueStrings(
    array
) {

    return [
        ...new Set(
            array
                .map(
                    item =>
                        String(item).trim()
                )
                .filter(
                    item => item.length > 0
                )
        )
    ];

}