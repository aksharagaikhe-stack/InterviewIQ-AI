const signupForm = document.getElementById("signupForm");
const signupStatus = document.getElementById("signupStatus");

signupForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const education = document.getElementById("education").value.trim();
    const skills = document.getElementById("skills").value.trim();

    if (!name || !email || !password) {
        signupStatus.textContent = "Please fill in all required fields.";
        return;
    }

    if (password.length < 6) {
        signupStatus.textContent =
            "Password must be at least 6 characters.";
        return;
    }

    signupStatus.textContent = "Creating your account...";

    try {

        const response = await fetch(`${API_URL}/api/signup`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password,
                education: education,
                skills: skills
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            signupStatus.textContent =
                data.message || "Unable to create account.";
            return;
        }

        signupStatus.textContent =
            "Account created successfully!";

        localStorage.setItem("student_id", data.student_id);

        localStorage.setItem(
            "student_profile",
            JSON.stringify({
                id: data.user_id,
                name: name,
                email: email,
                education: education,
                skills: skills
            })
        );

        setTimeout(() => {
            window.location.href = "dashboard.html";
        }, 700);

    } catch (error) {

        console.error("SIGNUP ERROR:", error);

        signupStatus.textContent =
            "Failed to connect to the server. Make sure the backend is running.";
    }
});
