var obj_button;
var obj_id;
var obj_num;
var obj_status;

var worker;
var worked_working = false;

function check_support_worker(){
	if(typeof(Worker) !== "undefined")
	    return true;
	add_status("Sorry! No Web Worker support. Update your browser!");
    return false;
}

function add_status(str){
	obj_status.innerHTML += str+"<br>";
}

function launch_worker(){
	worker = new Worker("../static/js/worker.js");
    worker.onmessage = function (event) {
    	var data = event.data;
    	switch (data.messageType){
    		case 'start':
    			obj_id.innerHTML = data.id;
    			obj_num.innerHTML = data.num;
    			add_status("Запущено: num=" +data.num.toString());
    			change_content_start();
    			break;
    		case 'progress':
    			add_status(data.current_num.toString()+" checking...");
    			break;
    		case 'result':
    			add_status("Знайдено просте число: " + data.data);
    			change_content_stop();
    			break;
    		default:
    			break;
    	};
    };
    worker.postMessage("start");
} 

function change_content_start(){
	obj_button.disabled = false;
	worked_working = true;
	obj_button.innerHTML="Відключитись";
}

function change_content_stop(){
	obj_button.disabled = false;
	worked_working = false;
	obj_button.innerHTML="Підключитись";
}

function button_con(){
	obj_button.disabled = true;
    if (worked_working == false){
    	add_status("Запуск...");
    	if (check_support_worker() == false)
    		return;
		launch_worker();
		setTimeout(function (){ obj_button.disabled = false; },5)
	}else{
		add_status("Зупинено");
		worker.terminate();
		change_content_stop();
	}
}

function test(){
	var val =  BigInteger("15415648545184489789789788");
	var val2 =  BigInteger("154156485451844897897897");
	var val5 =  BigInteger("154156485451844897897896");
	var val3 = BigInteger(2);

	var d = 2;
	//alert(val2);
	//alert(val2.add(val5));
	//alert(val2);
	//alert(val4.compareAbs(val4));
	//alert(val4);
	//alert(val2.remainder(val5));
	//alert(val2.add(1));
	//alert(val.compareAbs("15415648545184489789789788"));
}

window.onload=function(){	
	test();
	obj_button = document.getElementById("button_con");
	obj_id = document.getElementById("id");
	obj_num = document.getElementById("num");
	obj_status = document.getElementById("status");
}