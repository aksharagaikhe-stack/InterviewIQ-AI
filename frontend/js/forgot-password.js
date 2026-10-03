
const forgotForm = document.getElementById("forgotPasswordForm");
const forgotStatus = document.getElementById("forgotStatus");

forgotForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const email = document.getElementById("email").value.trim();

    if (!email) {
        forgotStatus.textContent = "Please enter your email.";
        return;
    }

    forgotStatus.textContent = "Processing request...";

    try {

        const response = await fetch(
            `${API_URL}/api/forgot-password`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email
                })
            }
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            forgotStatus.textContent =
                data.message || "Unable to process request.";
            return;
        }

        if (data.reset_token) {

            sessionStorage.setItem(
                "password_reset_token",
                data.reset_token
            );

            forgotStatus.textContent =
                "Reset token generated. Opening password reset page...";

            setTimeout(() => {
                window.location.href = "reset-password.html";
            }, 1000);

        } else {

            forgotStatus.textContent = data.message;

        }

    } catch (error) {

        console.error("FORGOT PASSWORD ERROR:", error);

        forgotStatus.textContent =
            "Failed to connect to the server. Make sure the backend is running.";

    }

});