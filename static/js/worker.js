var xmlhttp;
var id;
var start_num;
var end_num;
var session;

var val;
var check_timer;
var connect_timer;
var xmlhttp;

onmessage = function (event) {
	var data = event.data;
	importScripts("BigInteger.js");
	xmlhttp = getXmlHttp();
	setTimeout(start,100);
};


function start(){
	xmlhttp.open('GET', '/worker?type=start', false);
	xmlhttp.send(null);
	if(xmlhttp.status != 200){
		send_connection_error();
		setTimeout(start, 5000);
	}
	else{
		id = xmlhttp.responseText;
		postMessage({
			"messageType":"start",
			"id":id,
		});
		get_work();
	}
}


function get_work(){
	xmlhttp.open('GET', '/worker?type=get_work&id='+id, false);
	xmlhttp.send(null);
	if (xmlhttp.status == 200){
		if (xmlhttp.responseText != 'no_work'){
			param = JSON.parse(xmlhttp.responseText);
			param_data = param.data
			start_num = bigInt(param_data["start_num"])
			session = param["session"]
			end_num = bigInt(start_num.add(bigInt(param_data["count_num"]-1)))
			postMessage({
					"messageType":"get_work",
					"work":true,
					"num_start":param_data["start_num"],
					"num_end":end_num.toString(),
					"session":session,
				});
			work();
			return;
		}
		else{
			postMessage({
				"messageType":"get_work",
				"work":false,
			});
		}
	} else send_connection_error();
	setTimeout(get_work, 5000);
}

function send_connection_error(){
	postMessage({
		"messageType":"connectError"
	});
}

function send_test(val){
	postMessage({
		"messageType":"test",
		"val":val
	});
}

function work(param){
	var current_num;
	for(var current_num=start_num;current_num.compare(end_num)==-1;current_num=current_num.add(2)){
		if (current_num.isPrime()==true){
			postMessage({
				"messageType":"result",
				"current_num":current_num.toString(),
			});
			xmlhttp.open('GET', '/worker?type=find&id='+id+'&session='+session+'&prime='+current_num.toString(), false);
			xmlhttp.send(null);
			if (xmlhttp.status != 200)
				send_connection_error();
			setTimeout(get_work,5000);
			return;
		}
	}

	postMessage({"messageType":"end_to_check",});
	xmlhttp.open('GET', '/worker?type=check&session='+session+'&id='+id,false);
	xmlhttp.send(null);
	if (xmlhttp.status == 200){
		if (xmlhttp.responseText != "ok"){
			setTimeout(get_work,2000);
			return;
		}
	}else
		send_connection_error();
	setTimeout(get_work,500);
}


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

function setParameters(dict){

}