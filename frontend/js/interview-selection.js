// ======================================================
// InterviewIQ AI
// Interview Selection JavaScript
// ======================================================
const studentId = localStorage.getItem("student_id");

if (!studentId) {
    window.location.href = "login.html";
}

document.addEventListener("DOMContentLoaded", function () {

    // ==================================================
    // ELEMENTS
    // ==================================================

    const interviewType =
        document.getElementById(
            "interviewType"
        );

    const category =
        document.getElementById(
            "category"
        );

    const language =
        document.getElementById(
            "language"
        );

    const role =
        document.getElementById(
            "role"
        );

    const difficulty =
        document.getElementById(
            "difficulty"
        );

    const questionCount =
        document.getElementById(
            "questionCount"
        );

    const startButton =
        document.getElementById(
            "startInterviewBtn"
        );

    const statusMessage =
        document.getElementById(
            "statusMessage"
        );


    // ==================================================
    // GET STUDENT ID
    // ==================================================

    function getStudentId() {

        return localStorage.getItem(
            "student_id"
        );

    }


    // ==================================================
    // MESSAGE
    // ==================================================

    function showStatus(message) {

        if (statusMessage) {

            statusMessage.textContent =
                message;

        }

    }


    // ==================================================
    // LANGUAGE VISIBILITY
    // ==================================================

    function updateLanguageVisibility() {

        if (!language || !interviewType) {
            return;
        }


        const type =
            interviewType.value;


        if (
            type === "coding" ||
            type === "mixed"
        ) {

            language.disabled = false;

        } else {

            language.disabled = true;

            language.value = "";

        }

    }


    // ==================================================
    // CATEGORY VISIBILITY
    // ==================================================

    function updateCategoryVisibility() {

        if (!category || !interviewType) {
            return;
        }


        const type =
            interviewType.value;


        if (type === "technical") {

            category.disabled = false;

        } else {

            category.disabled = true;


            if (type === "hr") {

                category.value =
                    "Behavioral";

            }

            else if (type === "coding") {

                category.value =
                    "Programming";

            }

            else if (type === "mixed") {

                category.value =
                    "Mixed";

            }

            else {

                category.value = "";

            }

        }

    }


    // ==================================================
    // INTERVIEW TYPE CHANGE
    // ==================================================

    if (interviewType) {

        interviewType.addEventListener(
            "change",
            function () {

                updateLanguageVisibility();

                updateCategoryVisibility();

            }
        );

    }


    updateLanguageVisibility();

    updateCategoryVisibility();


    // ==================================================
    // START INTERVIEW
    // ==================================================

    if (!startButton) {

        console.error(
            "Start interview button not found."
        );

        return;

    }


    startButton.addEventListener(
        "click",
        async function () {

            // ==========================================
            // STUDENT ID
            // ==========================================

            const studentId =
                getStudentId();


            if (!studentId) {

    showStatus(
        "Please login first."
    );

    setTimeout(function () {

        window.location.href =
            "login.html";

    }, 800);

    return;

}


            // ==========================================
            // GET VALUES
            // ==========================================

            const selectedType =
                interviewType
                    ? interviewType.value
                    : "technical";


            const selectedRole =
                role
                    ? role.value
                    : "Software Developer";


            const selectedDifficulty =
                difficulty
                    ? difficulty.value
                    : "Medium";


            const selectedCount =
                questionCount
                    ? Number(questionCount.value)
                    : 10;


            // ==========================================
            // CATEGORY
            // ==========================================

            let selectedCategory = null;


            if (selectedType === "technical") {

                selectedCategory =
                    category
                        ? category.value
                        : "";

                if (!selectedCategory) {

                    showStatus(
                        "Please select a technical category."
                    );

                    return;

                }

            }

            else if (selectedType === "hr") {

                selectedCategory =
                    "Behavioral";

            }

            else if (selectedType === "coding") {

                selectedCategory =
                    "Programming";

            }

            else if (selectedType === "mixed") {

                selectedCategory =
                    "Mixed";

            }


            // ==========================================
            // LANGUAGE
            // ==========================================

            let selectedLanguage =
                null;


            if (
                selectedType === "coding" ||
                selectedType === "mixed"
            ) {

                selectedLanguage =
                    language
                        ? language.value
                        : "";


                if (!selectedLanguage) {

                    showStatus(
                        "Please select a programming language."
                    );

                    return;

                }

            }


            // ==========================================
            // QUESTION COUNT
            // ==========================================

            if (
                !Number.isInteger(
                    selectedCount
                ) ||
                selectedCount < 1 ||
                selectedCount > 20
            ) {

                showStatus(
                    "Question count must be between 1 and 20."
                );

                return;

            }


            // ==========================================
            // REQUEST DATA
            // ==========================================

            const requestData = {

                student_id:
                    Number(studentId),

                interview_type:
                    selectedType,

                category:
                    selectedCategory,

                role:
                    selectedRole,

                difficulty:
                    selectedDifficulty,

                language:
                    selectedLanguage,

                question_count:
                    selectedCount

            };


            console.log(
                "Starting interview:",
                requestData
            );


            // ==========================================
            // DISABLE BUTTON
            // ==========================================

            startButton.disabled = true;

            startButton.textContent =
                "Preparing Interview...";


            showStatus(
                "AI is preparing your personalized interview..."
            );


            // ==========================================
            // SEND REQUEST
            // ==========================================

            try {

                const response =
                    await fetch(
                        `${API_URL}/api/interview/start`,
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
                        "Unable to start interview."
                    );

                }


                // ======================================
                // SAVE INTERVIEW
                // ======================================

                if (!data.interview) {

                    throw new Error(
                        "Interview data was not returned."
                    );

                }


                localStorage.setItem(
                    "interview_data",

                    JSON.stringify(
                        data.interview
                    )
                );


                // ======================================
                // SUCCESS
                // ======================================

                showStatus(
                    "Interview ready!"
                );


                window.location.href =
                    "interview.html";


            } catch (error) {

                console.error(
                    "Interview Start Error:",
                    error
                );


                showStatus(
                    error.message ||
                    "Unable to start interview."
                );


                startButton.disabled = false;

                startButton.textContent =
                    "Start Interview";

            }

        }
    );

});