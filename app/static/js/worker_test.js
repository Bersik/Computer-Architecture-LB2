var xmlhttp;
var id;
var num;
var count_num;
var session;

var val;
var check_timer;
var connect_timer;
var xmlhttp;

onmessage = function (event) {
    importScripts("biginteger.js");
    xmlhttp = getXmlHttp();
    start();
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
		if (xmlhttp.responseText != 'error'){
			param = JSON.parse(xmlhttp.responseText);
			num = param["num"]
			count_num = param["count_num"]
			session = param["session"]
			postMessage({
				"messageType":"get_work",
				"work":true,
				"num":num,
				"count_num":count_num,
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

function work(){
	var current_num = BigInteger(num);
	var end_num = current_num.add(count_num);
	var send_count_iterations = BigInteger("1000000");
	var numbers =[];

	for(var current_num = BigInteger(num);current_num.compare(end_num)==-1;){
		numbers.push(current_num);
		current_num = current_num.add(2);
	}
	
	//якщо число досить велике, то ділим порціями по send_count_iterations елементів
	if (end_num.quotient(2).compare(send_count_iterations)==1){
		var BigTwo = BigInteger(2);
		for(var i=0;i<numbers.length;i++){
			var k = BigInteger(3);
			var k_end;
			var current_num = numbers[i];
			var not_prime=false;


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
							"iteration":k.toString()
						});
				xmlhttp.open('GET', '/worker?type=check&session='+session+'&id='+id, false);
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
			//знайшли
						postMessage({
							"messageType":"result",
							"current_num":current_num.toString(),
						});

						xmlhttp.open('GET', '/worker?type=find&session='+session+'&prime='+current_num.toString(), false);
						xmlhttp.send(null);
						if (xmlhttp.status == 200)
							setTimeout(get_work,5000);
						else 
							send_connection_error();
						return;
}
		}
		setTimeout(get_work,2000);
	}
}


function check(){
	xmlhttp.open('GET', '/worker?type=check', false);
	xmlhttp.send(null);
	if(xmlhttp.status == 200) {
	  	param = JSON.parse(xmlhttp.responseText);
	  	if (param["search"] == true){
	  		clearInterval(check_timer);
	  		var num = BigInteger(param["num"])
	  		var count_op = BigInteger(param["count_op"])

	  		
	  		val = BigInteger(param["num"]);
			id = param["id"];
			if (val.remainder(2).compareAbs(0)==0)
				pos = val.add(1);
			else
				pos = val.add(2);
			postMessage({
				"messageType":"start",
				"id":id,
				"num":BigInteger.toString(val),
				"current_num":BigInteger.toString(pos)
			});
			running = true;
	    	exit_(f());
	    	set_interval_check();
	  	}
		
	}	
}


function exit_(num){
	postMessage({"messageType":"result","data":BigInteger.toString(num)});
	close();
}

function progress(running){
	postMessage({
        		"messageType":"progress",
        		"current_num":BigInteger.toString(pos)
    });
}

function f(){
	while(true){
		progress(running);
		if (isprime(pos)==true){
			return pos;
		}
		pos = pos.add(2);
	}
}

function isprime(n){
    if(n.compareAbs(1)==0) // 1 - не простое число
        return false;
    var d=BigInteger(2);
    while(d.multiply(d).compareAbs(n)==-1){
        // если разделилось нацело, то составное
        if(n.remainder(d).compareAbs(0)==0) 
            return false;
        
        d=d.add(1);
    }
    // если нет нетривиальных делителей, то простое
    return true;
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