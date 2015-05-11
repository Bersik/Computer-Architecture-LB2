var obj_button_search;
var obj_number;
var obj_clients;
var xmlhttp;


function getXmlHttp(){
  var xmlhttp;
  try {
    xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
  } catch (e) {
    try {
      xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    } catch (E) {
      xmlhttp = false;
    }
  }
  if (!xmlhttp && typeof XMLHttpRequest!='undefined') {
    xmlhttp = new XMLHttpRequest();
  }
  return xmlhttp;
}


function search(){
	if (obj_button.innerHTML === "Пошук"){
		xmlhttp.open('GET', '/server?num='+obj_number.value, true);
		obj_prime_num.innerHTML="";
		xmlhttp.onreadystatechange = function(){
			if ((xmlhttp.readyState == 4) && (xmlhttp.status == 200)) {
       			obj_button.innerHTML = "Зупинити";
  			}
		};
		xmlhttp.send(null);
	}else{
		xmlhttp.open('GET', '/server?stop=true', true);
		xmlhttp.send(null);
		xmlhttp.onreadystatechange = function(){
			if ((xmlhttp.readyState == 4) && (xmlhttp.status == 200)) {
       			obj_button.innerHTML = "Пошук";
  			}
		};
	}
}

function update(){
	xmlhttp.open('GET', '/server?update=true', true);
	xmlhttp.onreadystatechange = function(){
		if ((xmlhttp.readyState == 4) && (xmlhttp.status == 200)) {
			parameters = JSON.parse(xmlhttp.responseText);
       		clients = parameters.clients
			obj_clients.options.length = 0;
			for (var client in clients){
				client_str = client + ") IP: " + clients[client].ip
				if (clients[client].start_num){
					client_str+="; початкове число: " +clients[client].start_num
				}
				obj_clients.options[obj_clients.options.length] = new Option(client_str,client);
			}
			log = parameters.log
			obj_status.innerHTML = "";
			for(var i in log){
				obj_status.innerHTML += log[i] + "<br/>";
			}
			obj_status.scrollTop = obj_status.scrollHeight;
			if (parameters.prime != undefined){
				obj_prime_num.innerHTML = parameters.prime;
				obj_button.innerHTML = "Пошук";
			}
  		}
	};
	xmlhttp.send(null);
}

function get_random(){
	xmlhttp.open('GET', '/server?get_random=true', true);
	xmlhttp.onreadystatechange = function(){
		if ((xmlhttp.readyState == 4) && (xmlhttp.status == 200)){
			if (xmlhttp.responseText!="")
				obj_number.innerHTML=xmlhttp.responseText;
		}
	}
	xmlhttp.send(null);
}

window.onload=function(){	
	obj_button = document.getElementById("button_search");
	obj_number = document.getElementById("number");
	obj_status = document.getElementById("status");
	obj_clients = document.getElementById("clients");
	obj_prime_num = document.getElementById("prime_num");
	xmlhttp = getXmlHttp();
	setInterval("update();",5000);
	update();
}

function add_status(str){
	obj_status.innerHTML += str+"<br>";
	//obj_status.scrollTop = obj_status.scrollHeight;
}