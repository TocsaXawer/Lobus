const image = document.getElementById("thumbnail{{ data[3] }}");
const lightbox = document.getElementById("lightbox");

image.addEventListener("click", () => {
    lightbox.style.display = "flex"; // Megjeleníti a lightbox-ot
});

function closeLightbox() {
    lightbox.style.display = "none"; // Elrejti a lightbox-ot
}
