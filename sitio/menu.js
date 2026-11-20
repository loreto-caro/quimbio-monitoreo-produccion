// 1. Buscamos el botón y el menú en la página
const boton = document.querySelector(".boton-menu");
const menu = document.querySelector(".menu");

// 2. Al hacer clic en el botón, abrimos o cerramos el menú
boton.addEventListener("click", () => {
    const abierto = menu.classList.toggle("menu-abierto");
    boton.setAttribute("aria-expanded", abierto);
    boton.textContent = abierto ? "✕" : "☰";
});

// 3. Al elegir una sección, cerramos el menú
menu.querySelectorAll("a").forEach((enlace) => {
    enlace.addEventListener("click", () => {
        menu.classList.remove("menu-abierto");
        boton.setAttribute("aria-expanded", false);
        boton.textContent = "☰";
    });
});