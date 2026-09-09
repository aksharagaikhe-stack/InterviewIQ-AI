// ======================================================
// InterviewIQ AI
// Student Profile JavaScript
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

    const profileForm = document.getElementById("profileForm");
    const statusMessage = document.getElementById("statusMessage");

    if (!profileForm) {
        console.error("Profile form not found.");
        return;
    }

    // ==================================================
    // CHECK LOGIN
    // ==================================================

    const studentId = localStorage.getItem("student_id");

    if (!studentId) {
        window.location.href = "login.html";
        return;
    }

    // ==================================================
    // LOAD EXISTING PROFILE
    // ==================================================

    loadProfile(studentId);


    // ==================================================
    // FORM SUBMISSION
    // ==================================================

    profileForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const education = document.getElementById("education").value.trim();
        const skills = document.getElementById("skills").value.trim();

        // ==================================================
        // VALIDATION
        // ==================================================

        if (!name) {
            showMessage("Please enter your name.", "error");
            return;
        }

        if (!email) {
            showMessage("Please enter your email.", "error");
            return;
        }

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            showMessage("Please enter a valid email address.", "error");
            return;
        }

        // ==================================================
        // BUTTON
        // ==================================================

        const submitButton =
            profileForm.querySelector('button[type="submit"]');

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Saving Profile...";
        }

        // ==================================================
        // PROFILE DATA
        // ==================================================

        const profileData = {
            name: name,
            email: email,
            education: education,
            skills: skills,
            student_id: Number(studentId)
        };

        console.log("Sending profile:", profileData);

        // ==================================================
        // SEND TO BACKEND
        // ==================================================

        try {

            const response = await fetch(
                `${API_URL}/api/student`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(profileData)
                }
            );

            console.log("HTTP Status:", response.status);

            const data = await response.json();

            console.log("Backend Response:", data);

            // ==================================================
            // CHECK RESPONSE
            // ==================================================

            if (!response.ok || !data.success) {

                throw new Error(
                    data.message || "Unable to save profile."
                );
            }

            // ==================================================
            // GET STUDENT ID
            // ==================================================

            const savedStudentId =
                data.student_id || studentId;

            // ==================================================
            // SAVE STUDENT ID
            // ==================================================

            localStorage.setItem(
                "student_id",
                String(savedStudentId)
            );

            // ==================================================
            // SAVE PROFILE LOCALLY
            // ==================================================

            const profile = {
                id: savedStudentId,
                name: name,
                email: email,
                education: education,
                skills: skills
            };

            localStorage.setItem(
                "student_profile",
                JSON.stringify(profile)
            );

            // ==================================================
            // SUCCESS MESSAGE
            // ==================================================

            showMessage(
                "Profile saved successfully!",
                "success"
            );

            // ==================================================
            // MOVE TO INTERVIEW SELECTION
            // ==================================================

            setTimeout(() => {

                window.location.href =
                    "interview-selection.html";

            }, 800);

        } catch (error) {

            console.error(
                "Profile Error:",
                error
            );

            showMessage(
                error.message ||
                "Unable to connect to the backend.",
                "error"
            );

            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = "Save Profile";
            }
        }
    });
});


// ======================================================
// LOAD EXISTING PROFILE
// ======================================================

async function loadProfile(studentId) {

    try {

        const response = await fetch(
            `${API_URL}/api/student/${studentId}`
        );

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        console.log("Existing profile:", data);

        if (!data.success || !data.student) {
            return;
        }

        const student = data.student;

        const nameElement =
            document.getElementById("name");

        const emailElement =
            document.getElementById("email");

        const educationElement =
            document.getElementById("education");

        const skillsElement =
            document.getElementById("skills");

        if (nameElement && student.name) {
            nameElement.value = student.name;
        }

        if (emailElement && student.email) {
            emailElement.value = student.email;
        }

        if (educationElement && student.education) {
            educationElement.value = student.education;
        }

        if (skillsElement && student.skills) {
            skillsElement.value = student.skills;
        }

    } catch (error) {

        console.log(
            "Could not load existing profile:",
            error
        );
    }
}


// ======================================================
// SHOW MESSAGE
// ======================================================

function showMessage(message, type) {

    const messageElement =
        document.getElementById("statusMessage");

    if (!messageElement) {
        console.log(message);
        return;
    }

    messageElement.textContent = message;

    if (type === "success") {
        messageElement.className = "success-message";
    } else {
        messageElement.className = "error-message";
    }
}