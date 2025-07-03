var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  });
}

function CargaHtml(contenido,clave){
    $('#'+contenido).load(clave);

}
function SubMenuC(campo, Titu) {
  const elemento = document.getElementById(campo);
  if (elemento) {
    // Crear contenedor del submenú
    const li = document.createElement("li");
    li.innerHTML = `
      <span class="caret">${Titu}</span>
      <ul class="nested"></ul>
    `;
    elemento.appendChild(li);
  }
}

function CargaOpcion(campo, ruta, dest, titu, sgv) {
  const submenu = document.getElementById(`${campo}-submenu`);
  if (submenu) {
    const li = document.createElement("li");
    li.innerHTML = `
      <span style="cursor:pointer" onclick="window.open('${ruta}', '${dest}')">
        ${titu}
      </span>
    `;
    submenu.appendChild(li);
  } else {
    console.error("No se encontró el submenú con id:", `${campo}-submenu`);
  }
}
