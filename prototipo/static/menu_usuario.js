var http_request = new XMLHttpRequest();
var url = "http://127.0.0.1:8000/captchaprot/ver_colecciones";
http_request.open("GET", url, true);
http_request.send();
http_request.onreadystatechange = function() {
    if (http_request.readyState == 4) {
		if (http_request.status == 200) {
			var json_data = http_request.responseText;
			dibujarTablaColecciones(JSON.parse(json_data));
		} else {
			alert("Ocurrió un problema con la URL.");
		}
		http_request = null;
	}
};

function dibujarTablaColecciones(datos) {
	var tbody = document.getElementById("cuerpo");
	for(let i = 0; i < datos.colecciones.length; i++) {
		var fila = document.createElement("tr");
		var nombre = document.createElement("td");
		var desc = document.createElement("td");
		var id = document.createElement("th");
		var pClave = document.createElement("td");
		var ver = document.createElement("td");
		var descargar = document.createElement("td");

		id.setAttribute("scope", "row");

		nombre.innerHTML = datos.colecciones[i].nombre;
		id.innerHTML = datos.colecciones[i].id_coleccion;
		desc.innerHTML = datos.colecciones[i].descripcion;

		var keywords = datos.colecciones[i].palabras_clave.split(";");

		for(let j = 0; j < keywords.length; j++) {
			var btn = document.createElement("BUTTON");
			btn.setAttribute("style", "pointer-events: none;");
			btn.setAttribute("class", "btn btn-sm btn-warning border");
			btn.innerHTML = keywords[j];
			pClave.append(btn);
		}

		var verBtn = document.createElement("BUTTON");
		verBtn.setAttribute("class", "btn btn-danger");
		verBtn.addEventListener("click", function() {
			var http_request = new XMLHttpRequest();
			var id = datos.colecciones[i].id_coleccion.toString();
			var url = "http://127.0.0.1:8000/captchaprot/ver_textos_coleccion?id_coleccion=" + id;
			http_request.open("GET", url, true);
			http_request.send();
			http_request.onreadystatechange = function() {
				if (http_request.readyState == 4) {
					if (http_request.status == 200) {
						var json_data = http_request.responseText;
						dialogoColeccion(JSON.parse(json_data), id);
					} else {
						alert("Ocurrió un problema con la URL.");
					}
					http_request = null;
				}
			};
		});
		verBtn.appendChild(document.createTextNode("Ver"));

		ver.appendChild(verBtn);

		var descargarBtn = document.createElement("BUTTON");
		descargarBtn.setAttribute("class", "btn btn-danger");
		descargarBtn.addEventListener("click", function() {
			var id = datos.colecciones[i].id_coleccion.toString();
			var url = "http://127.0.0.1:8000/captchaprot/descargar_csv?id_coleccion=" + id;
			location = url;
		});
		descargarBtn.appendChild(document.createTextNode("Descargar"));
		descargar.appendChild(descargarBtn);

		fila.appendChild(id);
		fila.appendChild(nombre);
		fila.appendChild(desc);
		fila.appendChild(pClave); 
		fila.appendChild(ver);
		fila.appendChild(descargar);

		tbody.appendChild(fila);
	}

}


function dialogoColeccion(retos, id) {
	
	document.getElementsByClassName("modal-title")[0].innerText = "Colección #" + id;
	
	var tbodySi = document.getElementById("cuerpo_si");
	for(let i = 0; i < retos.textos_etiquetados.length; i++) {
		var fila = document.createElement("tr");
		var text = document.createElement("td");
		var eleccion = document.createElement("td");
		var fiabilidad = document.createElement("td");
		
		text.innerHTML = retos.textos_etiquetados[i].texto;
		eleccion.innerHTML = retos.textos_etiquetados[i].eleccion;
		fiabilidad.innerHTML = retos.textos_etiquetados[i].fiabilidad;

		fila.appendChild(text);
		fila.appendChild(eleccion);
		fila.appendChild(fiabilidad);
		tbodySi.appendChild(fila);
	}

	var tbodyNo = document.getElementById("cuerpo_no");
	for(let i = 0; i < retos.textos_sin_etiquetar.length; i++) {
		var fila = document.createElement("tr");
		var text = document.createElement("td");
		var fiabilidad = document.createElement("td");

		text.innerHTML = retos.textos_sin_etiquetar[i].texto;
		fiabilidad.innerHTML = retos.textos_sin_etiquetar[i].fiabilidad;

		fila.appendChild(text);
		fila.appendChild(fiabilidad);
		tbodyNo.appendChild(fila);
	}
	
	const myModal = document.getElementById("ventana_dialogo");
	const modal = new bootstrap.Modal(myModal);
	modal.show();
}