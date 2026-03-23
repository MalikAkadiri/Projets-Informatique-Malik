
let nav = document.getElementById("header");

window.addEventListener("scroll", () => {
    if (window.scrollY > 25) {
        nav.classList.add("scrolled");
    }
    else {
        if (nav.classList.contains("scrolled")) {
            nav.classList.remove("scrolled");
        }
    }
});