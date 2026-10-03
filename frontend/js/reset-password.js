
const resetForm = document.getElementById("resetPasswordForm");
const resetStatus = document.getElementById("resetStatus");

resetForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const newPassword =
        document.getElementById("newPassword").value;

    const confirmPassword =
        document.getElementById("confirmPassword").value;

    const token = sessionStorage.getItem(
        "password_reset_token"
    );

    if (!token) {
        resetStatus.textContent =
            "Reset session expired. Please request a new reset link.";
        return;
    }

    if (newPassword.length < 6) {
        resetStatus.textContent =
            "Password must be at least 6 characters.";
        return;
    }

    if (newPassword !== confirmPassword) {
        resetStatus.textContent =
            "Passwords do not match.";
        return;
    }

    resetStatus.textContent = "Updating password...";

    try {

        const response = await fetch(
            `${API_URL}/api/reset-password`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    token: token,
                    new_password: newPassword
                })
            }
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            resetStatus.textContent =
                data.message || "Unable to reset password.";
            return;
        }

        sessionStorage.removeItem("password_reset_token");

        resetStatus.textContent =
            "Password reset successfully! Redirecting to login...";

        resetForm.reset();

        setTimeout(() => {
            window.location.href = "login.html";
        }, 1500);

    } catch (error) {

        console.error("RESET PASSWORD ERROR:", error);

        resetStatus.textContent =
            "Failed to connect to the server. Make sure the backend is running.";

    }

});