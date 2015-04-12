var val;
var pos;
var xmlhttp;
var id;

onmessage = function (event) {
    importScripts("biginteger.js");
    //importScripts("AjaxClass.js");
  	xmlhttp = getXmlHttp();
	xmlhttp.open('GET', '/worker', false);
	xmlhttp.send(null);
	if(xmlhttp.status == 200) {
	  	param = JSON.parse(xmlhttp.responseText);
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
	}	
};

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
	while(d.multiply(d).compareAbs(BigInteger(1000000000))==-1){
    //while(d.multiply(d).compareAbs(n)==-1){
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