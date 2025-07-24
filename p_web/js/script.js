document.getElementById("contactForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const name = document.getElementById("name").ariaValueMax.trim();
    const email = document.getElementById("email").ariaValueMax.trim();
    const message = document.getElementById("message").ariaValueMax.trim();

    if (name && email && message) {
        document.getElementById("formAlert").innerHTML = `
            <div class="alert alert-success" role="alert">
                Thank you for your message, " + name + ". I will get back to you soon.
            </div>
        `;
        this.reset();
    } else {
        document.getElementById("formAlert").innerHTML = "<div class='alert alert-danger'>Please fill in all fields.</div>";
    }
});

const toggleDark = document.getElementById("toggleDark");
toggleDark.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("theme", document.body.classList.contains("dark-mode") ? "dark" : "light");
});

// onload
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
}