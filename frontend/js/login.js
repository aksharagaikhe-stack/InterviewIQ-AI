const loginForm = document.getElementById("loginForm");
const loginStatus = document.getElementById("loginStatus");

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        loginStatus.textContent =
            "Please enter your email and password.";
        return;
    }

    loginStatus.textContent = "Logging in...";

    try {

        const response = await fetch(`${API_URL}/api/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            loginStatus.textContent =
                data.message || "Invalid email or password.";
            return;
        }

        localStorage.setItem("student_id", data.user.student_id);
        

        localStorage.setItem(
            "student_profile",
            JSON.stringify(data.user)
        );

        loginStatus.textContent =
            "Login successful!";

        setTimeout(() => {
            window.location.href = "dashboard.html";
        }, 500);

    } catch (error) {

        console.error("LOGIN ERROR:", error);

        loginStatus.textContent =
            "Failed to connect to the server. Make sure the backend is running.";
    }
});