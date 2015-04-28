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
	switch (data){
		case 'start':
		importScripts("biginteger.js");
		xmlhttp = getXmlHttp();
		setTimeout(start,100);
		break;
		default:
		break;
	}
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
			start_num = BigInteger(param_data["start_num"])
			session = param["session"]
			end_num = BigInteger(start_num.add(BigInteger(param_data["count_num"]-1)))
			postMessage({
					"messageType":"get_work",
					"work":true,
					"num_start":param_data["start_num"],
					"num_end":BigInteger.toString(end_num),
					"session":session,
				});
			if (param["stopped"] == true)
				work(param_data);
			else
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
	var send_count_iterations = BigInteger("100000");
	var numbers =[];
	var current_num;

	for(current_num=start_num;current_num.compare(end_num)==-1;){
		numbers.push(current_num);
		current_num = current_num.add(2);
	}
	
	if (current_num.compare(BigInteger(9007199254))==-1){
		send_count_iterations = BigInteger(Math.sqrt(BigInteger.toString(current_num)))
	}
	var i=0;
	var BigTwo = BigInteger(2);
	var k = BigInteger(3);

	if (param!= undefined){
		i = param["i"]-1;
		k = BigInteger(param["iteration"]);
	}

	for(;i<numbers.length;i++){
		
		var k_end;
		var current_num = numbers[i];
		var not_prime=false;
		postMessage({
			"messageType":"began_to_check",
			"current_num":current_num.toString(),
			"current_i":i+1,
			"len":numbers.length
		});
		do{
			k_end = k.add(send_count_iterations);
			while(k.compare(k_end)==-1){
				if(current_num.remainder(k).compareAbs(0)==0){
					not_prime=true
					break;
				}
				k = k.add(BigTwo);
			}
			postMessage({
				"messageType":"progress",
				"current_num":current_num.toString(),
				"iteration":k.toString(),
				"not_prime":not_prime
			});
			xmlhttp.open('GET', '/worker?type=check&session='+session+
				'&id='+id+
				"&i="+(i+1)+
				"&count="+numbers.length+
				"&current_num="+current_num.toString()+
				"&not_prime="+not_prime+
				"&iteration="+k.toString(),
				false);
			xmlhttp.send(null);
			if (xmlhttp.status == 200){
				if (xmlhttp.responseText != "ok"){
					setTimeout(get_work,2000);
					return;
				}
			}else
			send_connection_error();
			k=k_end;
			if (not_prime)
				break;
		}while(k.multiply(k).compare(current_num)!=1)

		if (not_prime == false){
			postMessage({
				"messageType":"result",
				"current_num":current_num.toString(),
			});

			xmlhttp.open('GET', '/worker?type=find&id='+id+'&session='+session+'&prime='+current_num.toString(), false);
			xmlhttp.send(null);
			if (xmlhttp.status == 200)
				setTimeout(get_work,5000);
			else 
				send_connection_error();
			return;
		}
		k = BigInteger(3);
	}
	setTimeout(get_work,2000);
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