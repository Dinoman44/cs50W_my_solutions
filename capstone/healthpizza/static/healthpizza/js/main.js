document.addEventListener("DOMContentLoaded", () => {
    let smolscreen_navbar = document.querySelector("#smolscreen-navbar");
    smolscreen_navbar.hidden = "none";
    document.querySelector("#phone-footer").hidden = "none";
    document.querySelector("#logo-png").addEventListener("click", () => window.location = "/")
})