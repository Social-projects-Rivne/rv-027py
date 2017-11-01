'use strict';


var btn = document.getElementById('deleteMe');
var idToDelete = 2;
var jsontoSend = JSON.stringify(idToDelete);

function show() {
	alert(jsontoSend);
	var req = new XMLHttpRequest();
	req.open('GET', '/index', true);
	req.send();
	window.location.href = '/index';
}

btn.addEventListener('click', show);