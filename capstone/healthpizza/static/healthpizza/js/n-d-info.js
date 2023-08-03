document.addEventListener("DOMContentLoaded", () => {
    let pbq = document.querySelector("#pbq");
    let solution = document.querySelector("#solution");
    pbq.addEventListener("click", () => {
        solution.style.display = "inline";
    })
})