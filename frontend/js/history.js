// ======================================================
// InterviewIQ AI
// Interview History JavaScript
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    loadHistory
);


// ======================================================
// LOAD HISTORY
// ======================================================

async function loadHistory() {

    const studentId =
        localStorage.getItem(
            "student_id"
        );


    const container =
        document.getElementById(
            "historyContainer"
        );


    if (!studentId) {

        if (container) {

            container.innerHTML = `

                <div class="empty-history">

                    <h3>
                        Student profile not found
                    </h3>

                    <p>
                        Please create your profile
                        before viewing interview history.
                    </p>

                    <button onclick="goToProfile()">
                        Create Profile
                    </button>

                </div>

            `;

        }

        return;

    }


    try {

        const response =
            await fetch(
                `${API_URL}/api/interview/history/${studentId}`
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.message ||
                "Unable to load history."
            );

        }


        const history =
            Array.isArray(
                data.history
            )
                ? data.history
                : [];


        // ==========================================
        // DISPLAY
        // ==========================================

        displayProgress(
            history
        );


        displayAnalytics(
            history
        );


        displayHistory(
            history
        );


    } catch (error) {

        console.error(
            "History Error:",
            error
        );


        if (container) {

            container.innerHTML = `

                <div class="empty-history">

                    <h3>
                        Unable to load history
                    </h3>

                    <p>
                        Please make sure the backend
                        server is running.
                    </p>

                    <button onclick="loadHistory()">
                        Try Again
                    </button>

                </div>

            `;

        }

    }

}


// ======================================================
// PROGRESS
// ======================================================

function displayProgress(
    history
) {

    const totalElement =
        document.getElementById(
            "totalInterviews"
        );


    const averageElement =
        document.getElementById(
            "averageScore"
        );


    const bestElement =
        document.getElementById(
            "bestScore"
        );


    const latestElement =
        document.getElementById(
            "latestScore"
        );


    const messageElement =
        document.getElementById(
            "progressMessage"
        );


    if (
        !history ||
        history.length === 0
    ) {

        setText(
            totalElement,
            "0"
        );

        setText(
            averageElement,
            "0.0"
        );

        setText(
            bestElement,
            "0.0"
        );

        setText(
            latestElement,
            "0.0"
        );


        if (messageElement) {

            messageElement.innerHTML = `

                <div class="no-progress">

                    <h3>
                        No interview data yet
                    </h3>

                    <p>
                        Complete an interview to start
                        tracking your progress.
                    </p>

                </div>

            `;

        }

        return;

    }


    // ==============================================
    // SCORES
    // ==============================================

    const scores =
        history.map(
            function (item) {

                return Number(
                    item.overall_score || 0
                );

            }
        );


    const total =
        scores.length;


    const average =
        scores.reduce(
            function (
                sum,
                score
            ) {

                return sum + score;

            },
            0
        ) / total;


    const best =
        Math.max(
            ...scores
        );


    const latest =
        scores[0];


    const first =
        scores[
            scores.length - 1
        ];


    const improvement =
        latest - first;


    // ==============================================
    // DISPLAY
    // ==============================================

    setText(
        totalElement,
        String(total)
    );


    setText(
        averageElement,
        average.toFixed(1)
    );


    setText(
        bestElement,
        best.toFixed(1)
    );


    setText(
        latestElement,
        latest.toFixed(1)
    );


    // ==============================================
    // MESSAGE
    // ==============================================

    if (!messageElement) {
        return;
    }


    if (improvement > 0) {

        messageElement.innerHTML = `

            <div class="progress-positive">

                <h3>
                    📈 You're improving!
                </h3>

                <p>
                    Your latest score is
                    <strong>
                        ${improvement.toFixed(1)}
                    </strong>
                    points higher than your
                    first interview.
                </p>

            </div>

        `;

    }

    else if (improvement < 0) {

        messageElement.innerHTML = `

            <div class="progress-negative">

                <h3>
                    💪 Keep practicing!
                </h3>

                <p>
                    Your latest score is
                    ${Math.abs(
                        improvement
                    ).toFixed(1)}
                    points lower than your first interview.
                </p>

            </div>

        `;

    }

    else {

        messageElement.innerHTML = `

            <div class="progress-neutral">

                <h3>
                    🎯 Keep going!
                </h3>

                <p>
                    Your performance is currently stable.
                    Continue practicing to improve.
                </p>

            </div>

        `;

    }

}


// ======================================================
// ANALYTICS
// ======================================================

function displayAnalytics(
    history
) {

    const container =
        document.getElementById(
            "analyticsContainer"
        );


    if (!container) {
        return;
    }


    if (
        !history ||
        history.length === 0
    ) {

        container.innerHTML = `

            <div class="no-progress">

                <p>
                    No analytics available yet.
                </p>

            </div>

        `;

        return;

    }


    const latest =
        history[0];


    const analytics = [

        {
            name:
                "Technical",

            score:
                latest.technical_score
        },

        {
            name:
                "Communication",

            score:
                latest.communication_score
        },

        {
            name:
                "Relevance",

            score:
                latest.relevance_score
        },

        {
            name:
                "Grammar",

            score:
                latest.grammar_score
        },

        {
            name:
                "Clarity",

            score:
                latest.clarity_score
        }

    ];


    container.innerHTML = "";


    analytics.forEach(
        function (item) {

            const score =
                Number(
                    item.score || 0
                );


            const percentage =
                Math.max(
                    0,
                    Math.min(
                        100,
                        score * 10
                    )
                );


            const row =
                document.createElement(
                    "div"
                );


            row.className =
                "analytics-row";


            row.innerHTML = `

                <div class="analytics-label">

                    <span>
                        ${escapeHTML(
                            item.name
                        )}
                    </span>

                    <strong>
                        ${score.toFixed(1)}/10
                    </strong>

                </div>


                <div class="progress-bar">

                    <div
                        class="progress-fill"
                        style="width:${percentage}%">
                    </div>

                </div>

            `;


            container.appendChild(
                row
            );

        }
    );

}


// ======================================================
// HISTORY CARDS
// ======================================================

function displayHistory(
    history
) {

    const container =
        document.getElementById(
            "historyContainer"
        );


    if (!container) {
        return;
    }


    if (
        !history ||
        history.length === 0
    ) {

        container.innerHTML = `

            <div class="empty-history">

                <h3>
                    No interviews yet
                </h3>

                <p>
                    Complete your first AI interview
                    to see your performance here.
                </p>

                <button onclick="startInterview()">
                    Start Interview
                </button>

            </div>

        `;

        return;

    }


    container.innerHTML = "";


    history.forEach(
        function (item) {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "history-card";


            const score =
                Number(
                    item.overall_score || 0
                );


            const type =
                capitalize(
                    item.interview_type
                );


            const category =
                item.category ||
                "General";


            card.innerHTML = `

                <div class="history-top">

                    <div>

                        <h3>
                            ${escapeHTML(
                                item.role ||
                                "Software Developer"
                            )}
                        </h3>

                        <p>
                            ${escapeHTML(
                                type
                            )}
                        </p>

                    </div>


                    <div class="score">

                        ${score.toFixed(1)}/10

                    </div>

                </div>


                <div class="history-details">

                    <span>
                        Category:
                        ${escapeHTML(
                            category
                        )}
                    </span>


                    <span>
                        Difficulty:
                        ${escapeHTML(
                            item.difficulty ||
                            "N/A"
                        )}
                    </span>


                    <span>
                        Language:
                        ${escapeHTML(
                            item.language ||
                            "N/A"
                        )}
                    </span>


                    <span>
                        Questions:
                        ${Number(
                            item.question_count || 0
                        )}
                    </span>

                </div>


                <div class="history-date">

                    ${formatDate(
                        item.created_at
                    )}

                </div>

            `;


            container.appendChild(
                card
            );

        }
    );

}


// ======================================================
// CAPITALIZE
// ======================================================

function capitalize(
    text
) {

    if (!text) {
        return "";
    }


    return (
        text.charAt(0).toUpperCase() +
        text.slice(1)
    );

}


// ======================================================
// FORMAT DATE
// ======================================================

function formatDate(
    dateString
) {

    if (!dateString) {

        return "Unknown date";

    }


    try {

        let normalized =
            String(
                dateString
            ).trim();


        // SQLite format:
        // YYYY-MM-DD HH:MM:SS

        if (
            normalized.includes(" ") &&
            !normalized.includes("T")
        ) {

            normalized =
                normalized.replace(
                    " ",
                    "T"
                );

        }


        const date =
            new Date(
                normalized
            );


        if (
            Number.isNaN(
                date.getTime()
            )
        ) {

            return dateString;

        }


        return date.toLocaleString();

    } catch (error) {

        return dateString;

    }

}


// ======================================================
// ESCAPE HTML
// ======================================================

function escapeHTML(
    value
) {

    return String(
        value ?? ""
    )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

}


// ======================================================
// SET TEXT
// ======================================================

function setText(
    element,
    value
) {

    if (element) {

        element.textContent =
            value;

    }

}


// ======================================================
// NAVIGATION
// ======================================================

function startInterview() {

    window.location.href =
        "interview-selection.html";

}


function goToProfile() {

    window.location.href =
        "profile.html";

}


function goHome() {

    window.location.href =
        "index.html";

}