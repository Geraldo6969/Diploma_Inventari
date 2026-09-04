document.addEventListener("DOMContentLoaded", function () {
    document.title = "E Inventory";

    document.querySelectorAll(".brand-text, .navbar-brand, #site-name a").forEach(function (element) {
        element.textContent = "E Inventory";
    });
});
