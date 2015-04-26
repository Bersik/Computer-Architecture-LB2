var obj_button;
var obj_id;
var obj_num;
var obj_status;
var timer_online;
var xmlhttp;
var id;
var session;

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
	obj_status.scrollTop = obj_status.scrollHeight;
}

function launch_worker(){
	worker = new Worker("../static/js/worker.js");
    worker.onmessage = function (event) {
    	var data = event.data;
    	switch (data.messageType){
    		case 'connectError':
    			add_status("Помилка підключення...");
    			break;
    		case 'start':
    			obj_id.innerHTML = data.id;
    			id=data.id;
    			add_status("Підлючився. Мій id - "+data.id+".");
    			document.title = "Клієнт №"+ data.id
    			change_content_start();
    			break;
    		case 'get_work':
    			if (data.work == true){
    				obj_num.innerHTML = data.num_start;
    				add_status("Запустив пошук. Початкове число - " +data.num_start+". Кінцеве число - " +data.num_end+ ". Сессія - "+data.session+".");
    			}
    			else{
    				add_status("Роботи немає. Очікую...");
    			}
    			break;
    		case 'began_to_check':
    			add_status("Починаю перевіряти число "+data.current_num+" ("+data.current_i+"/"+data.len+").");
    			break;
    		case 'progress':
    			if (data.not_prime){
    				add_status("Число "+data.current_num+" складене. Ділиться на "+data.iteration+".");
    			}else{
    				add_status("Продовжую перевіряти число "+data.current_num+". Зараз ділю на "+data.iteration+".");
    			}
    			break;
    		case 'result':
    			add_status("Я знайшов просте число! Це " + data.current_num+".");
    			break;
    		case 'test':
    			add_status("Тест! val="+data.val);
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
	timer_online = setInterval(online,5000);
	online();
}

function change_content_stop(){
	obj_button.disabled = false;
	worked_working = false;
	obj_button.innerHTML="Підключитись";
	clearInterval(timer_online);
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
		worker.terminate();
		xmlhttp = new XMLHttpRequest();
		xmlhttp.open('GET', '/worker?type=stop&id='+id, true);
		xmlhttp.send(null);
		change_content_stop();
		add_status("Зупинено");
	}
}

window.onload=function(){	
	obj_button = document.getElementById("button_con");
	obj_id = document.getElementById("id");
	obj_num = document.getElementById("num");
	obj_status = document.getElementById("status");
}

function online(){
	xmlhttp = new XMLHttpRequest();
	xmlhttp.open('GET', '/worker?type=online&id='+id, true);
	xmlhttp.send(null);
}