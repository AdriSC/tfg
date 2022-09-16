//var myOb = JSON.parse('{"reto": [{"id": 8, "text": "ejemplo challenge 8", "options": ["opcion1", "opcion2", "opcion3"]}, {"id": 4, "text": "ejemplo challenge 4", "options": ["opcion1", "opcion2", "opcion3"]}, {"id": 3, "text": "ejemplo challenge 3", "options": ["opcion1", "opcion2", "opcion3"]}]}');
var i = 0;
var myObj;
var objRes = JSON.parse('{"respuestas":[]}');
var http_request;
var url = "http://127.0.0.1:8000/captchaprot/reto"; // Esta URL debería devolver datos JSON
var url1 = "http://127.0.0.1:8000/captchaprot/comprobacion";
var xhr;
var empezar, siguiente, enviar;
const div = document.getElementById("div_principal");
var button_group;
var retoh1;
var div_ct = document.createElement("div");
var output = document.createElement("p");
var ops = document.createElement("div");
var primero = true;

requisitos = {
	palabras_clave: "pablo iglesias,real madrid",
	palabras_restringidas: "monasterio",
	num_textos: 5
}
	
retoh1 = document.createElement("h1")
retoh1.style.fontFamily = "'Product Sans', sans-serif";
retoh1.innerHTML = "¿Eres un robot?";
div.appendChild(retoh1);

output.setAttribute("class", "p-output");
div_ct.appendChild(output);
div.appendChild(div_ct);
output.innerHTML = "<br>";

div.setAttribute("id", "este_div")
div.appendChild(ops);

function hacerRequest(primero) {
	http_request = new XMLHttpRequest();
	http_request.open("POST", url, true);
	http_request.setRequestHeader("Accept", "application/json");
	http_request.setRequestHeader('Content-Type', 'application/json');
	http_request.onreadystatechange = handle_json;
	http_request.send(JSON.stringify(requisitos));
}
	
hacerRequest();

function crearBoton(){
	if(primero) {
		empezar = document.createElement("BUTTON");
		var t = document.createTextNode("No");
		empezar.appendChild(t);
		div.appendChild(empezar);
		empezar.addEventListener("click", () => {
			mostrarMensaje();
		});
	}
	else {
		mostrarMensaje();
	}
}

function handle_json() {
	if (http_request.readyState == 4) {
		if (http_request.status == 200) {
			var json_data = http_request.responseText;
			myObj = JSON.parse(json_data);
			crearBoton();
		} else {
			alert("Ocurrió un problema con la URL.");
		}
		http_request = null;
	}
}

function mostrarMensaje() {
	retoh1.remove();
	empezar.style.display = "none";

	output.style.fontSize = '18px';
	output.innerHTML = myObj.reto[i].text;

	for(var j = 0; j < myObj.reto[i].options.length; j++) {
		if(button_group === undefined) {
			button_group = document.createElement("div");
			button_group.setAttribute("class", "btn-group");
		}

		var op1 = document.createElement("BUTTON");
		var t = document.createTextNode(myObj.reto[i].options[j]);
		op1.appendChild(t);
		op1.setAttribute("name", "opcion");
		op1.addEventListener("click", function() {
			if(i < myObj.reto.length - 1){
				procesarResultado(j);
				output.innerHTML = nextItem();
				mostrarMensaje();
			}
			else{
				procesarResultado(j);
				button_group.remove();
				enviarResultado();
			}
		})
		button_group.appendChild(op1);
		div.appendChild(button_group);
	}
}

function nextItem() {
	i = i + 1; 
	button_group.style.display = "none";
	button_group = undefined;
	return myObj.reto[i].text; 
}

function mostrarExito(){
	if (xhr.readyState == 4) {
		if (xhr.status == 200) {
			var res = JSON.parse(xhr.responseText);
			if (res["resultado"] == "correcto") {
				window.top.postMessage('hello', '*');
			}
			else if (res["resultado"] == "incorrecto") {
				output.innerHTML = "Inténtalo de nuevo";
				var retryBtn = document.createElement("button");
				var t = document.createTextNode("Reintentar");
				retryBtn.appendChild(t);
				div.appendChild(retryBtn);
				retryBtn.addEventListener("click", function() {
					retryBtn.remove();
					hacerRequest();
				});
			}
		} else {
				alert("Ocurrió un problema con la URL.");
		}
		xhr = null;
	}
}

function enviarResultado(){
	i = 0;
	if(primero) primero = false;
	xhr = new XMLHttpRequest();
	xhr.onreadystatechange = mostrarExito;
	xhr.open("POST", url1, true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify(objRes));
}

function procesarResultado(j){
	var newStr = '{"id":' + myObj.reto[i].id + ',"respuesta":' + myObj.reto[i].options[j] + "}";
	objRes.respuestas.push(JSON.parse(newStr));
}

