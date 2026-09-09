// ======================================================
// InterviewIQ AI
// Final Report JavaScript
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        // ==============================================
        // LOAD DATA
        // ==============================================

        const reportStorage =
            localStorage.getItem(
                "interview_report"
            );

        const interviewStorage =
            localStorage.getItem(
                "interview_data"
            );


        if (
            !reportStorage ||
            !interviewStorage
        ) {

            alert(
                "Interview report not found."
            );

            window.location.href =
                "interview-selection.html";

            return;

        }


        let report;

        let interviewData;


        try {

            report =
                JSON.parse(
                    reportStorage
                );

            interviewData =
                JSON.parse(
                    interviewStorage
                );

        } catch (error) {

            console.error(
                "Report parsing error:",
                error
            );


            alert(
                "Invalid report data."
            );


            window.location.href =
                "interview-selection.html";

            return;

        }


        // ==============================================
        // DISPLAY
        // ==============================================

        displayStudentInformation(
            interviewData
        );


        displayScores(
            report
        );


        displayPerformanceMessage(
            report
        );


        displayFeedback(
            report
        );


        const analysis =
            generatePerformanceAnalysis(
                report
            );


        displayStrengths(
            report.strengths?.length
                ? report.strengths
                : analysis.strengths
        );


        displayWeaknesses(
            report.weaknesses?.length
                ? report.weaknesses
                : analysis.weaknesses
        );


        const suggestions =
            generatePersonalizedSuggestions(
                report
            );


        displaySuggestions(
            suggestions
        );


        const skillGaps =
            generateSkillGaps(
                report,
                interviewData
            );


        displaySkillGaps(
            skillGaps
        );


        // ==============================================
        // ACTION BUTTONS
        // ==============================================

        setupActionButtons();


        // ==============================================
        // SAVE HISTORY
        // ==============================================

        saveInterviewHistory(
            report,
            interviewData
        );

    }
);


// ======================================================
// STUDENT INFORMATION
// ======================================================

function displayStudentInformation(
    interviewData
) {

    const profile =
        interviewData.student_profile ||
        {};


    const studentName =
        document.getElementById(
            "studentName"
        );


    if (studentName) {

        studentName.textContent =
            profile.name ||
            "Student";

    }


    const role =
        document.getElementById(
            "role"
        );


    if (role) {

        role.textContent =
            interviewData.role ||
            "Software Developer";

    }


    const interviewType =
        document.getElementById(
            "interviewType"
        );


    if (interviewType) {

        interviewType.textContent =
            formatType(
                interviewData.interview_type
            );

    }


    const category =
        document.getElementById(
            "category"
        );


    if (category) {

        category.textContent =
            interviewData.category ||
            "—";

    }


    const difficulty =
        document.getElementById(
            "difficulty"
        );


    if (difficulty) {

        difficulty.textContent =
            interviewData.difficulty ||
            "—";

    }


    const language =
        document.getElementById(
            "language"
        );


    if (language) {

        language.textContent =
            interviewData.language ||
            "Not Applicable";

    }


    const details =
        document.getElementById(
            "interviewDetails"
        );


    if (details) {

        details.textContent =
            `${interviewData.role || "Software Developer"} • ` +
            `${formatType(interviewData.interview_type)} • ` +
            `${interviewData.category || "General"} • ` +
            `${interviewData.difficulty || "Medium"} • ` +
            `${interviewData.language || "N/A"}`;

    }

}


// ======================================================
// FORMAT TYPE
// ======================================================

function formatType(
    type
) {

    const map = {

        technical:
            "Technical",

        coding:
            "Coding",

        hr:
            "HR",

        mixed:
            "Mixed"

    };


    return (
        map[type] ||
        "Interview"
    );

}


// ======================================================
// DISPLAY SCORES
// ======================================================

function displayScores(
    report
) {

    setScore(
        "overallScore",
        report.overall_score
    );


    setScore(
        "technicalScore",
        report.technical_score
    );


    setScore(
        "communicationScore",
        report.communication_score
    );


    setScore(
        "relevanceScore",
        report.relevance_score
    );


    setScore(
        "grammarScore",
        report.grammar_score
    );


    setScore(
        "clarityScore",
        report.clarity_score
    );

}


// ======================================================
// SET SCORE
// ======================================================

function setScore(
    id,
    score
) {

    const element =
        document.getElementById(
            id
        );


    if (!element) {
        return;
    }


    element.textContent =
        Number(
            score || 0
        ).toFixed(1);

}


// ======================================================
// PERFORMANCE MESSAGE
// ======================================================

function displayPerformanceMessage(
    report
) {

    const element =
        document.getElementById(
            "performanceMessage"
        );


    if (!element) {
        return;
    }


    const score =
        Number(
            report.overall_score || 0
        );


    if (score >= 8) {

        element.textContent =
            "Excellent performance! Keep improving.";

    }

    else if (score >= 6) {

        element.textContent =
            "Good performance. A little more practice will help.";

    }

    else if (score >= 4) {

        element.textContent =
            "Average performance. Focus on your weak areas.";

    }

    else {

        element.textContent =
            "Keep practicing. You can improve significantly.";

    }

}


// ======================================================
// FEEDBACK
// ======================================================

function displayFeedback(
    report
) {

    const elements = [

        document.getElementById(
            "feedback"
        ),

        document.getElementById(
            "aiFeedback"
        )

    ];


    elements.forEach(
        function (element) {

            if (element) {

                element.textContent =
                    report.feedback ||
                    "Keep practicing and improving your interview answers.";

            }

        }
    );

}


// ======================================================
// PERFORMANCE ANALYSIS
// ======================================================

function generatePerformanceAnalysis(
    report
) {

    const strengths = [];

    const weaknesses = [];


    const technical =
        Number(
            report.technical_score || 0
        );


    const communication =
        Number(
            report.communication_score || 0
        );


    const relevance =
        Number(
            report.relevance_score || 0
        );


    const grammar =
        Number(
            report.grammar_score || 0
        );


    const clarity =
        Number(
            report.clarity_score || 0
        );


    if (technical >= 8) {

        strengths.push(
            "Strong technical knowledge"
        );

    }


    if (communication >= 8) {

        strengths.push(
            "Good communication skills"
        );

    }


    if (relevance >= 8) {

        strengths.push(
            "Answers are highly relevant"
        );

    }


    if (grammar >= 8) {

        strengths.push(
            "Good grammatical accuracy"
        );

    }


    if (clarity >= 8) {

        strengths.push(
            "Clear and well-structured answers"
        );

    }


    if (technical < 6) {

        weaknesses.push(
            "Technical concepts need improvement"
        );

    }


    if (communication < 6) {

        weaknesses.push(
            "Communication skills need improvement"
        );

    }


    if (relevance < 6) {

        weaknesses.push(
            "Answers should be more relevant and focused"
        );

    }


    if (grammar < 6) {

        weaknesses.push(
            "Grammar and sentence structure need improvement"
        );

    }


    if (clarity < 6) {

        weaknesses.push(
            "Answers should be clearer and better structured"
        );

    }


    if (strengths.length === 0) {

        strengths.push(
            "You demonstrated a good foundation of interview skills."
        );

    }


    if (weaknesses.length === 0) {

        weaknesses.push(
            "No major weakness detected."
        );

    }


    return {

        strengths:
            strengths,

        weaknesses:
            weaknesses

    };

}


// ======================================================
// DISPLAY STRENGTHS
// ======================================================

function displayStrengths(
    strengths
) {

    const containers = [

        document.getElementById(
            "strengths"
        ),

        document.getElementById(
            "strengthsList"
        )

    ];


    containers.forEach(
        function (container) {

            if (!container) {
                return;
            }


            container.innerHTML = "";


            strengths.forEach(
                function (item) {

                    const li =
                        document.createElement(
                            "li"
                        );


                    li.textContent =
                        item;


                    container.appendChild(
                        li
                    );

                }
            );

        }
    );

}


// ======================================================
// DISPLAY WEAKNESSES
// ======================================================

function displayWeaknesses(
    weaknesses
) {

    const containers = [

        document.getElementById(
            "weaknesses"
        ),

        document.getElementById(
            "weaknessesList"
        )

    ];


    containers.forEach(
        function (container) {

            if (!container) {
                return;
            }


            container.innerHTML = "";


            weaknesses.forEach(
                function (item) {

                    const li =
                        document.createElement(
                            "li"
                        );


                    li.textContent =
                        item;


                    container.appendChild(
                        li
                    );

                }
            );

        }
    );

}


// ======================================================
// PERSONALIZED SUGGESTIONS
// ======================================================

function generatePersonalizedSuggestions(
    report
) {

    const suggestions = [];


    const technical =
        Number(
            report.technical_score || 0
        );


    const communication =
        Number(
            report.communication_score || 0
        );


    const relevance =
        Number(
            report.relevance_score || 0
        );


    const grammar =
        Number(
            report.grammar_score || 0
        );


    const clarity =
        Number(
            report.clarity_score || 0
        );


    if (Array.isArray(
        report.suggestions
    )) {

        suggestions.push(
            ...report.suggestions
        );

    }


    if (
        technical < 6
    ) {

        suggestions.push(
            "Revise core technical concepts related to your selected role."
        );

        suggestions.push(
            "Practice technical interview questions regularly."
        );

    }


    if (
        communication < 6
    ) {

        suggestions.push(
            "Practice explaining technical concepts aloud using simple language."
        );

    }


    if (
        relevance < 6
    ) {

        suggestions.push(
            "Focus on answering exactly what the interviewer asks."
        );

    }


    if (
        grammar < 6
    ) {

        suggestions.push(
            "Practice speaking using complete and grammatically correct sentences."
        );

    }


    if (
        clarity < 6
    ) {

        suggestions.push(
            "Structure answers using introduction, explanation, example and conclusion."
        );

    }


    if (suggestions.length === 0) {

        suggestions.push(
            "Excellent performance! Try a higher difficulty interview."
        );

        suggestions.push(
            "Continue practicing regularly."
        );

    }


    return [
        ...new Set(
            suggestions.filter(
                item => item
            )
        )
    ];

}


// ======================================================
// DISPLAY SUGGESTIONS
// ======================================================

function displaySuggestions(
    suggestions
) {

    const containers = [

        document.getElementById(
            "suggestions"
        ),

        document.getElementById(
            "suggestionsList"
        )

    ];


    containers.forEach(
        function (container) {

            if (!container) {
                return;
            }


            container.innerHTML = "";


            suggestions.forEach(
                function (item) {

                    const li =
                        document.createElement(
                            "li"
                        );


                    li.textContent =
                        item;


                    container.appendChild(
                        li
                    );

                }
            );

        }
    );

}


// ======================================================
// SKILL GAP ANALYSIS
// ======================================================

function generateSkillGaps(
    report,
    interviewData
) {

    const gaps = [];


    const technical =
        Number(
            report.technical_score || 0
        );


    const communication =
        Number(
            report.communication_score || 0
        );


    const relevance =
        Number(
            report.relevance_score || 0
        );


    const grammar =
        Number(
            report.grammar_score || 0
        );


    const clarity =
        Number(
            report.clarity_score || 0
        );


    if (technical < 6) {

        gaps.push({

            skill:
                "Technical Knowledge",

            score:
                technical,

            priority:
                technical < 4
                    ? "High"
                    : "Medium",

            recommendation:
                "Study core technical concepts and practice role-specific questions."

        });

    }


    if (communication < 6) {

        gaps.push({

            skill:
                "Communication",

            score:
                communication,

            priority:
                communication < 4
                    ? "High"
                    : "Medium",

            recommendation:
                "Practice speaking clearly and explaining concepts in your own words."

        });

    }


    if (relevance < 6) {

        gaps.push({

            skill:
                "Answer Relevance",

            score:
                relevance,

            priority:
                relevance < 4
                    ? "High"
                    : "Medium",

            recommendation:
                "Focus on the exact question and avoid unnecessary information."

        });

    }


    if (grammar < 6) {

        gaps.push({

            skill:
                "Grammar",

            score:
                grammar,

            priority:
                grammar < 4
                    ? "High"
                    : "Medium",

            recommendation:
                "Practice sentence formation and grammatically correct communication."

        });

    }


    if (clarity < 6) {

        gaps.push({

            skill:
                "Answer Clarity",

            score:
                clarity,

            priority:
                clarity < 4
                    ? "High"
                    : "Medium",

            recommendation:
                "Use structured and concise answers."

        });

    }


    const role =
        interviewData.role ||
        "";


    const language =
        interviewData.language ||
        "";


    if (
        technical < 6 &&
        role
    ) {

        gaps.push({

            skill:
                `${role} Technical Preparation`,

            score:
                technical,

            priority:
                "High",

            recommendation:
                `Practice more ${role} interview questions and revise important concepts.`

        });

    }


    if (
        technical < 6 &&
        language
    ) {

        gaps.push({

            skill:
                `${language} Programming`,

            score:
                technical,

            priority:
                "Medium",

            recommendation:
                `Practice ${language} coding problems and strengthen its core concepts.`

        });

    }


    return gaps;

}


// ======================================================
// DISPLAY SKILL GAPS
// ======================================================

function displaySkillGaps(
    skillGaps
) {

    const container =
        document.getElementById(
            "skillGaps"
        );


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (
        !skillGaps ||
        skillGaps.length === 0
    ) {

        container.innerHTML = `

            <div class="no-skill-gap">

                <h3>
                    Excellent Performance!
                </h3>

                <p>
                    No major skill gaps were detected
                    in this interview.
                </p>

            </div>

        `;

        return;

    }


    skillGaps.forEach(
        function (gap) {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "skill-gap-card";


            const content =
                document.createElement(
                    "div"
                );


            content.className =
                "skill-gap-content";


            const heading =
                document.createElement(
                    "h3"
                );


            heading.textContent =
                gap.skill;


            const score =
                document.createElement(
                    "p"
                );


            score.textContent =
                `Score: ${
                    Number(
                        gap.score || 0
                    ).toFixed(1)
                }/10`;


            const recommendation =
                document.createElement(
                    "p"
                );


            recommendation.textContent =
                gap.recommendation;


            const priority =
                document.createElement(
                    "span"
                );


            priority.className =
                "priority";


            priority.textContent =
                gap.priority;


            content.appendChild(
                heading
            );

            content.appendChild(
                score
            );

            content.appendChild(
                recommendation
            );


            card.appendChild(
                content
            );

            card.appendChild(
                priority
            );


            container.appendChild(
                card
            );

        }
    );

}


// ======================================================
// SAVE HISTORY
// ======================================================

async function saveInterviewHistory(
    report,
    interviewData
) {

    const studentId =
        interviewData.student_id ||
        localStorage.getItem(
            "student_id"
        );


    if (!studentId) {

        console.warn(
            "Student ID not found."
        );

        return;

    }


    // ==============================================
    // PREVENT DUPLICATE SAVE
    // ==============================================

    const savedReportKey =
        localStorage.getItem(
            "saved_report_timestamp"
        );


    if (
        savedReportKey &&
        savedReportKey ===
        String(
            report.completed_at
        )
    ) {

        console.log(
            "This report has already been saved."
        );

        return;

    }


    // ==============================================
    // HISTORY DATA
    // ==============================================

    const historyData = {

        student_id:
            Number(studentId),

        interview_type:
            interviewData.interview_type,

        category:
            interviewData.category ||
            null,

        role:
            interviewData.role,

        difficulty:
            interviewData.difficulty,

        language:
            interviewData.language,

        question_count:
            interviewData.question_count ||
            report.total_questions ||
            0,

        overall_score:
            Number(
                report.overall_score || 0
            ),

        technical_score:
            Number(
                report.technical_score || 0
            ),

        communication_score:
            Number(
                report.communication_score || 0
            ),

        relevance_score:
            Number(
                report.relevance_score || 0
            ),

        grammar_score:
            Number(
                report.grammar_score || 0
            ),

        clarity_score:
            Number(
                report.clarity_score || 0
            ),

        strengths:
            report.strengths || [],

        weaknesses:
            report.weaknesses || [],

        suggestions:
            report.suggestions ||
            []

    };


    try {

        const response =
            await fetch(
                `${API_URL}/api/interview/history`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            historyData
                        )

                }
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            !data.success
        ) {

            console.error(
                "History save failed:",
                data.message
            );

            return;

        }


        console.log(
            "Interview history saved successfully."
        );


        if (data.history_id) {

            localStorage.setItem(
                "last_history_id",
                String(
                    data.history_id
                )
            );

        }


        localStorage.setItem(
            "saved_report_timestamp",
            String(
                report.completed_at
            )
        );


    } catch (error) {

        console.error(
            "History API Error:",
            error
        );

    }

}


// ======================================================
// ACTION BUTTONS
// ======================================================

function setupActionButtons() {

    const practiceButton =
        document.getElementById(
            "practiceAgain"
        );


    if (practiceButton) {

        practiceButton.addEventListener(
            "click",
            practiceAgain
        );

    }


    const historyButton =
        document.getElementById(
            "viewHistory"
        );


    if (historyButton) {

        historyButton.addEventListener(
            "click",
            function () {

                window.location.href =
                    "history.html";

            }
        );

    }


    const homeButton =
        document.getElementById(
            "backHome"
        );


    if (homeButton) {

        homeButton.addEventListener(
            "click",
            goHome
        );

    }

}


// ======================================================
// PRACTICE AGAIN
// ======================================================

function practiceAgain() {

    localStorage.removeItem(
        "interview_report"
    );


    localStorage.removeItem(
        "interview_data"
    );


    localStorage.removeItem(
        "saved_report_timestamp"
    );


    window.location.href =
        "interview-selection.html";

}


// ======================================================
// HOME
// ======================================================

function goHome() {

    window.location.href =
        "index.html";

}