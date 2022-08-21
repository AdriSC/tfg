//var myOb = JSON.parse('{"challenges": [{"id": 8, "text": "ejemplo challenge 8", "options": ["opcion1", "opcion2", "opcion3"]}, {"id": 4, "text": "ejemplo challenge 4", "options": ["opcion1", "opcion2", "opcion3"]}, {"id": 3, "text": "ejemplo challenge 3", "options": ["opcion1", "opcion2", "opcion3"]}]}');
var i = 0;
var http_request = new XMLHttpRequest();
var myObj;
var objRes = JSON.parse('{"respuestas":[]}');
//var newStr = "";
var url = "http://127.0.0.1:8000/captchaprot/reto"; // Esta URL debería devolver datos JSON
var url1 = "http://127.0.0.1:8000/captchaprot/comprobacion";
var xhr = new XMLHttpRequest();
var empezar, siguiente, enviar;
const div = document.getElementById("div_principal");
var button_group;

// Descarga los datos JSON del servidor.
/*
http_request.open("GET", url, true);
http_request.send();*/
http_request.onreadystatechange = handle_json;
requisitos = {
	palabras_clave: "pablo iglesias,real madrid",
	palabras_restringidas: "monasterio",
	num_retos: 5
}

http_request.open("POST", url, true);
http_request.setRequestHeader("Accept", "application/json");
http_request.setRequestHeader('Content-Type', 'application/json');
http_request.send(JSON.stringify(requisitos));

var retoh1 = document.createElement("h1");
//retoh1.style.fontFamily = '"Comic Sans MS", "Comic Sans", cursive';
retoh1.style.fontFamily = "'Product Sans', sans-serif";
retoh1.innerHTML = "¿Eres un robot?";
div.appendChild(retoh1);

var div_ct = document.createElement("div");
var output = document.createElement("p");
output.setAttribute("class", "p-output");
div_ct.appendChild(output);
div.appendChild(div_ct);
output.innerHTML = "<br>";

var ops = document.createElement("div");
div.setAttribute("id", "este_div")
div.appendChild(ops);

function crearBoton(){
	empezar = document.createElement("BUTTON");
	var t = document.createTextNode("No");
	empezar.appendChild(t);
	//div.appendChild(empezar);
	div.appendChild(empezar);
	empezar.addEventListener("click", () => {
		mostrarMensaje();
	});
}

function handle_json() {
	if (http_request.readyState == 4) {
		if (http_request.status == 200) {
			var json_data = http_request.responseText;
			myObj = JSON.parse(json_data)
			crearBoton();
		} else {
			alert("Ocurrió un problema con la URL.");
		}
		http_request = null;
	}
}

function mostrarMensaje() {

	retoh1.style.display = "none";
	empezar.style.display = "none";

	output.style.fontSize = '18px';
	output.innerHTML = myObj.challenges[i].text;

	//button_group.setAttribute("class", "btn-group");

	for(var j = 0; j < myObj.challenges[i].options.length; j++) {
		if(button_group === undefined) {
			button_group = document.createElement("div");
			button_group.setAttribute("class", "btn-group");
		}

		/*var varName = "res" + (j + 1);
		var op1 = document.createElement("INPUT");
		op1.setAttribute("type", "radio");
		op1.setAttribute("id", varName);
		op1.setAttribute("name", "opcion");
		op1.setAttribute("value", j);
		ops.appendChild(op1);
		console.log(j);
		console.log(varName);
		//const node = document.createTextNode(myObj.challenges[i].options[j]);
		document.getElementById(varName).after(myObj.challenges[i].options[j]);

		var varName = "res" + (j + 1);*/
		var op1 = document.createElement("BUTTON");
		var t = document.createTextNode(myObj.challenges[i].options[j]);
		op1.appendChild(t);
		//op1.setAttribute("id", varName);
		op1.setAttribute("name", "opcion");
		//op1.setAttribute("value", );
		op1.setAttribute("value", j);
		op1.addEventListener("click", function() {
			if(i < myObj.challenges.length - 1){
				procesarResultado(j);
				output.innerHTML = nextItem();
				mostrarMensaje();
			}
			else{
				//siguiente.style.display = "none";

				procesarResultado(j);
				output.textContent = "Reto terminado";
				button_group.style.display = "none";

				enviarResultado();

				/*ops.style.visibility = "hidden";

				enviar = document.createElement("BUTTON");
				var t = document.createTextNode("Enviar");
				enviar.appendChild(t);
				div.appendChild(enviar);
				enviar.addEventListener("click", );*/

			}
		})
		button_group.appendChild(op1);
		div.appendChild(button_group);
		//document.write("<br>");
		//document.getElementById(varName).after(myObj.challenges[i].options[j]);
	}

	//siguiente = document.createElement("BUTTON");
	//var t = document.createTextNode("Siguiente");
	//siguiente.appendChild(t);
	//div.appendChild(siguiente);

	/*siguiente.addEventListener("click", () => {

	});*/
}

function nextItem() {
	i = i + 1; // increase i by one
	button_group.style.display = "none";
	button_group = undefined;
	return myObj.challenges[i].text; // give us back the item of where we are now
}

function mostrar_exito(){
	if (xhr.readyState == 4) {
		if (xhr.status == 200) {
			output.innerHTML = xhr.responseText;
		} else {
				alert("Ocurrió un problema con la URL.");
		}
		xhr = null;
	}
	//enviar.style.display = "none";
}

function enviarResultado(){
	//var formData = new FormData();
	//formData.append("respuestas", );
	window.top.postMessage('hello', '*'); //CAMBIAR A mostrar_exito CUANDO FUNCIONE
	xhr.onreadystatechange = mostrar_exito;
	xhr.open("POST", url1, true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	//xhr.setRequestHeader('Content-Type', 'text/plain');
	xhr.send(JSON.stringify(objRes));
	//xhr.send(objRes);
	console.log(JSON.stringify(objRes));
	//document.getElementById("resultado").innerHTML = JSON.stringify(objRes);
}

function procesarResultado(j){
	/*const radioButtons = document.querySelectorAll('input[name="opcion"]');
	let selectedSize;
	for (const radioButton of radioButtons) {
		if (radioButton.checked) {
			selectedSize = radioButton.value;
			break;
		}
	}*/
	console.log(j);
	var newStr = '{"id":' + myObj.challenges[i].id + ',"a":' + j.toString() + "}";
	console.log(newStr);
	objRes.respuestas.push(JSON.parse(newStr));
}

