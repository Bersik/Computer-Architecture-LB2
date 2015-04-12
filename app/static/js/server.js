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
		
		xmlhttp.open('GET', '/server?num='+obj_number.value, false);
		xmlhttp.send(null);
		if(xmlhttp.status == 200) {
			obj_button.innerHTML = "Зупинити";
		}
	}else{
		xmlhttp.open('GET', '/server?stop=true', false);
		xmlhttp.send(null);
		if(xmlhttp.status == 200) {
			obj_button.innerHTML = "Пошук";
		}
	}
}

function update(){
	xmlhttp.open('GET', '/server?update=true', false);
	xmlhttp.send(null);
	if(xmlhttp.status == 200) {
		clients = JSON.parse(xmlhttp.responseText);
		obj_clients.options.length = 0;
		for (var client in clients){
			client_str = client + ") IP: " + clients[client].ip
			obj_clients.options[obj_clients.options.length] = new Option(client_str,client);
		}
	}
}

window.onload=function(){	
	obj_button = document.getElementById("button_search");
	obj_number = document.getElementById("number");
	obj_status = document.getElementById("status");
	obj_clients = document.getElementById("clients");
	xmlhttp = getXmlHttp();
	setInterval("update();",5000)
	update();
}
