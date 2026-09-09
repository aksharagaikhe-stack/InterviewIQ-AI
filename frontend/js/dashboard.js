const studentId = localStorage.getItem("student_id");

if (!studentId) {
    window.location.href = "login.html";
}

const studentProfile =
    JSON.parse(localStorage.getItem("student_profile")) || {};

const studentNameElement =
    document.getElementById("studentName");

const welcomeUser =
    document.getElementById("welcomeUser");

const totalInterviews =
    document.getElementById("totalInterviews");

const averageScore =
    document.getElementById("averageScore");

const bestScore =
    document.getElementById("bestScore");

const performanceStatus =
    document.getElementById("performanceStatus");

const recentInterviews =
    document.getElementById("recentInterviews");


/* ------------------------------
   Display Student Name
------------------------------ */

const name = studentProfile.name || "Student";

studentNameElement.textContent = name;
welcomeUser.textContent = name;


/* ------------------------------
   Navigation
------------------------------ */

function startInterview() {
    window.location.href = "interview-selection.html";
}

function openHistory() {
    window.location.href = "history.html";
}

document
    .getElementById("startInterviewBtn")
    .addEventListener("click", startInterview);

document
    .getElementById("newInterviewCard")
    .addEventListener("click", startInterview);

document
    .getElementById("emptyStartBtn")
    .addEventListener("click", startInterview);

document
    .getElementById("historyCard")
    .addEventListener("click", openHistory);

document
    .getElementById("viewAllHistory")
    .addEventListener("click", openHistory);


/* ------------------------------
   Logout
------------------------------ */

document
    .getElementById("logoutBtn")
    .addEventListener("click", function () {

        localStorage.removeItem("student_id");
        localStorage.removeItem("student_profile");
        localStorage.removeItem("interview_data");
        localStorage.removeItem("interview_report");
        localStorage.removeItem("interview_results");
        localStorage.removeItem("saved_report_timestamp");

        window.location.href = "login.html";
    });


/* ------------------------------
   Load Interview History
------------------------------ */

async function loadDashboardHistory() {

    try {

        const response = await fetch(
            `${API_URL}/api/interview/history/${studentId}`
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            return;
        }

        const history = data.history || [];

        updateStatistics(history);
        displayRecentInterviews(history);

    } catch (error) {

        console.error(
            "DASHBOARD HISTORY ERROR:",
            error
        );

    }
}


/* ------------------------------
   Statistics
------------------------------ */

function updateStatistics(history) {

    if (history.length === 0) {

        totalInterviews.textContent = "0";
        averageScore.textContent = "0.0";
        bestScore.textContent = "0.0";
        performanceStatus.textContent = "Start";

        return;
    }

    const scores = history
        .map(item => Number(item.overall_score) || 0);

    const total = scores.length;

    const average =
        scores.reduce(
            (sum, score) => sum + score,
            0
        ) / total;

    const best = Math.max(...scores);

    totalInterviews.textContent = total;

    averageScore.textContent =
        average.toFixed(1);

    bestScore.textContent =
        best.toFixed(1);

    if (average >= 8) {
        performanceStatus.textContent = "Excellent";
    } else if (average >= 6) {
        performanceStatus.textContent = "Good";
    } else if (average > 0) {
        performanceStatus.textContent = "Improving";
    } else {
        performanceStatus.textContent = "Start";
    }
}


/* ------------------------------
   Recent Interviews
------------------------------ */

function displayRecentInterviews(history) {

    if (history.length === 0) {
        return;
    }

    const recent = history.slice(0, 3);

    recentInterviews.innerHTML = "";

    recent.forEach(item => {

        const card = document.createElement("div");

        card.className = "recent-card";

        const category =
            item.category ||
            item.interview_type ||
            "Interview";

        const difficulty =
            item.difficulty || "Medium";

        const score =
            Number(item.overall_score || 0)
                .toFixed(1);

        const date =
            item.created_at
                ? new Date(item.created_at)
                    .toLocaleDateString()
                : "Recent";

        card.innerHTML = `
            <div>
                <h3>${escapeHTML(category)}</h3>
                <p>
                    ${escapeHTML(difficulty)}
                    • ${date}
                </p>
            </div>

            <div class="recent-score">
                ${score}/10
            </div>
        `;

        recentInterviews.appendChild(card);
    });
}


/* ------------------------------
   Safe HTML
------------------------------ */

function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* ------------------------------
   Start
------------------------------ */

loadDashboardHistory();