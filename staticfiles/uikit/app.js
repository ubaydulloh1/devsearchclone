// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
  hljs.highlightAll();
});
let alert__div = document.getElementById("alert")
let alert__close = document.getElementById("alert__close")

alert__close.addEventListener('click', () => {
  alert__div.style.display = "none";
})