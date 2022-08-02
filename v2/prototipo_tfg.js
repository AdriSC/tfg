

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
			       
			// Descarga los datos JSON del servidor.
			//http_request.onreadystatechange = handle_json;
			//http_request.open("GET", url, true);
			//http_request.send();

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
			retoh1.innerHTML = "Reto";
			div.appendChild(retoh1);

			var output = document.createElement("p");
			div.appendChild(output);

			var ops = document.createElement("div");
			div.appendChild(ops);

			function crearBoton(){	
				empezar = document.createElement("BUTTON");
				var t = document.createTextNode("Empezar");
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
						myObj = JSON.parse(json_data);
						crearBoton();
					} else {
						alert("Ocurrió un problema con la URL.");
					}
					http_request = null;
				}
			}

			function mostrarMensaje() {

				empezar.style.display = "none";
			
				output.innerHTML = myObj.challenges[i].text;	
				
				for(var j = 0; j < myObj.challenges[i].options.length; j++){
					var varName = "res" + (j + 1);
					var op1 = document.createElement("INPUT");
					op1.setAttribute("type", "radio");
					op1.setAttribute("id", varName);
					op1.setAttribute("name", "opcion");
					op1.setAttribute("value", myObj.challenges[i].options[j]);
					ops.appendChild(op1);
					document.getElementById(varName).after(myObj.challenges[i].options[j]);
				}

				/*var op1 = document.createElement("INPUT");
				op1.setAttribute("type", "radio");
				op1.setAttribute("id", "res1");
				op1.setAttribute("name", "opcion");
				op1.setAttribute("value", 0);
				div.appendChild(op1);
				document.getElementById("res1").after(myObj.challenges[i].options[0]);

				var op2 = document.createElement("INPUT");
				op2.setAttribute("type", "radio");
				op2.setAttribute("id", "res2");
				op2.setAttribute("name", "opcion");
				op2.setAttribute("value", 1);
				div.appendChild(op2);
				document.getElementById("res2").after(myObj.challenges[i].options[1]);

				var op3 = document.createElement("INPUT");
				op3.setAttribute("type", "radio");
				op3.setAttribute("id", "res3");
				op3.setAttribute("name", "opcion");
				op3.setAttribute("value", 2);
				div.appendChild(op3);
				document.getElementById("res3").after(myObj.challenges[i].options[2]);*/
		
				siguiente = document.createElement("BUTTON");
				var t = document.createTextNode("Siguiente");
				siguiente.appendChild(t);
				div.appendChild(siguiente);

				siguiente.addEventListener("click", () => {
					if(i < myObj.challenges.length - 1){ 
						procesarResultado();
						output.innerHTML = nextItem();
					}
					else{
						siguiente.style.display = "none";

						procesarResultado();
						output.textContent = "Reto terminado";

						ops.style.visibility = "hidden";

						enviar = document.createElement("BUTTON");
						var t = document.createTextNode("Enviar");
						enviar.appendChild(t);
						div.appendChild(enviar);
						enviar.addEventListener("click", enviarResultado);

					}
				});

			}

			function nextItem() {
				i = i + 1; // increase i by one
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
				enviar.style.display = "none";
			}
			
			function enviarResultado(){
				//var formData = new FormData();
				//formData.append("respuestas", );
				xhr.onreadystatechange = mostrar_exito;
				xhr.open("POST", url1, true);
				xhr.setRequestHeader("Accept", "application/json");
				xhr.setRequestHeader('Content-Type', 'application/json');
				xhr.send(JSON.stringify(objRes));
				//document.getElementById("resultado").innerHTML = JSON.stringify(objRes);
			}

			function procesarResultado(){
				const radioButtons = document.querySelectorAll('input[name="opcion"]');
            	let selectedSize;
				for (const radioButton of radioButtons) {
					if (radioButton.checked) {
						selectedSize = radioButton.value;
						console.log(radioButton.value)
						break;
					}
				}
				var newStr = JSON.stringify('{"id":' + myObj.challenges[i].id + ',"a":"' + selectedSize + '"}');
				objRes.respuestas[i] = JSON.parse(newStr);
			}
	