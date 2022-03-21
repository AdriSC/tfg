var myObj = JSON.parse('{"challenges": [{"id": 8, "text": "ejemplo challenge 8", "options": ["opcion1", "opcion2", "opcion3"]}, {"id": 4, "text": "ejemplo challenge 4", "options": ["opcion1", "opcion2", "opcion3"]}, {"id": 3, "text": "ejemplo challenge 3", "options": ["opcion1", "opcion2", "opcion3"]}]}');
			var i = 0;
			var http_request = new XMLHttpRequest();
			var myObj;
			var objRes = JSON.parse('{"respuestas":[]}');
			//var newStr = "";
			var url = "http://127.0.0.1:8000/captchaprot/reto"; // Esta URL debería devolver datos JSON
			const xhr = new XMLHttpRequest();
			
			// Descarga los datos JSON del servidor.
			http_request.onreadystatechange = handle_json;
			http_request.open("GET", url, true);
			http_request.send(null);
			
			//crearBoton();
			function handle_json() {
				if (http_request.readyState == 4) {
					if (http_request.status == 200) {
						var json_data = http_request.responseText; 
						myObj = JSON.parse(json_data);
						console.log(json_data);
						console.log(myObj);
						crearBoton();
					} else {
						alert("Ocurrió un problema con la URL.");
						
					}
					http_request = null;
				}
			}

			function crearBoton(){
				var empezar = document.createElement("BUTTON");
				var t = document.createTextNode("Empezar");
				empezar.appendChild(t);
				document.body.appendChild(empezar);
				empezar.addEventListener("click", () => {
					mostrarMensaje();
				});
			}

			function mostrarMensaje() {
			
				document.getElementById("pregunta").innerHTML = myObj.challenges[i].text;	
					
				var op1 = document.createElement("INPUT");
				op1.setAttribute("type", "radio");
				op1.setAttribute("id", "res1");
				op1.setAttribute("name", "opcion");
				op1.setAttribute("value", 0);
				document.body.appendChild(op1);
				document.getElementById("res1").after(myObj.challenges[i].options[0]);

				var op2 = document.createElement("INPUT");
				op2.setAttribute("type", "radio");
				op2.setAttribute("id", "res2");
				op2.setAttribute("name", "opcion");
				op2.setAttribute("value", 1);
				document.body.appendChild(op2);
				document.getElementById("res2").after(myObj.challenges[i].options[1]);

				var op3 = document.createElement("INPUT");
				op3.setAttribute("type", "radio");
				op3.setAttribute("id", "res3");
				op3.setAttribute("name", "opcion");
				op3.setAttribute("value", 2);
				document.body.appendChild(op3);
				document.getElementById("res3").after(myObj.challenges[i].options[2]);
		
				var siguiente = document.createElement("BUTTON");
				var t = document.createTextNode("Siguiente");
				siguiente.appendChild(t);
				document.body.appendChild(siguiente);

				
				siguiente.addEventListener("click", () => {
					if(i < myObj.challenges.length - 1){ 
						procesarResultado();
						document.getElementById("pregunta").innerHTML = nextItem();
						
					}
					else{
						
						procesarResultado();
						enviarResultado();
					}
				});

			}

			function nextItem() {
				i = i + 1; // increase i by one
				return myObj.challenges[i].text; // give us back the item of where we are now
			}

			function enviarResultado(){
				document.getElementById("pregunta").textContent = "Reto terminado";
				xhr.onreadystatechange = mostrar_exito;
				xhr.open("POST", url, true);
				xhr.setRequestHeader('Content-Type', 'application/json');
				xhr.send(JSON.stringify(objRes));
				//document.getElementById("resultado").innerHTML = JSON.stringify(objRes);
			}

			function mostrar_exito(){
				if (xhr.readyState == 4) {
					if (xhr.status == 200) {
						document.getElementById("output").innerHTML = xhr.responseText; 
					} else {
						 alert("Ocurrió un problema con la URL.");
					}
					http_request = null;
				}
			}


			function procesarResultado(){
				const radioButtons = document.querySelectorAll('input[name="opcion"]');

            	let selectedSize;
				for (const radioButton of radioButtons) {
					if (radioButton.checked) {
						selectedSize = radioButton.value;
						break;
					}
				}
				
				var newStr = '{"id":' + myObj.challenges[i].id + ',"a":' + selectedSize + "}";
				//document.getElementById("str").innerHTML = newStr;
				objRes.respuestas[i] = JSON.parse(newStr);
				//document.getElementById("output").innerHTML = selectedSize ? `You selected ${selectedSize}` : `You haven't selected any size`;

			}
