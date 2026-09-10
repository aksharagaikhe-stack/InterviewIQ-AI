// ======================================================
// InterviewIQ AI
// Main Website JavaScript
// ======================================================

document.addEventListener("DOMContentLoaded", function () {

    // ==================================================
    // LOGIN BUTTON
    // ==================================================

    const loginButton = document.querySelector(".login-btn");

    if (loginButton) {
        loginButton.addEventListener("click", function () {
            alert(
                function handleLogin() {
    window.location.href = "login.html";
}
            );
        });
    }


    // ==================================================
    // START / SIGNUP BUTTONS
    // ==================================================

    const startButtons = document.querySelectorAll(
        ".signup-btn, .primary-btn, .cta-btn"
    );

    startButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            // Do not call interview API here.
            // First create/select the student profile.

            window.location.href = "profile.html";
        });

    });


    // ==================================================
    // EXPLORE FEATURES
    // ==================================================

    const exploreButton =
        document.querySelector(".secondary-btn");

    if (exploreButton) {

        exploreButton.addEventListener("click", function () {

            const features =
                document.querySelector("#features");

            if (features) {

                features.scrollIntoView({
                    behavior: "smooth"
                });

            }

        });

    }


    // ==================================================
    // NAVIGATION LINKS
    // ==================================================

    const homeLinks =
        document.querySelectorAll('[data-page="home"]');

    homeLinks.forEach(function (link) {

        link.addEventListener("click", function () {
            window.location.href = "index.html";
        });

    });


    const profileLinks =
        document.querySelectorAll('[data-page="profile"]');

    profileLinks.forEach(function (link) {

        link.addEventListener("click", function () {
            window.location.href = "profile.html";
        });

    });


    const historyLinks =
        document.querySelectorAll('[data-page="history"]');

    historyLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            const studentId =
                localStorage.getItem("student_id");

            if (!studentId) {

                alert(
                    "Please create your profile first."
                );

                window.location.href =
                    "profile.html";

                return;
            }

            window.location.href =
                "history.html";
        });

    });

});