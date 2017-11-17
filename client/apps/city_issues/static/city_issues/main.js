(function(){

var map = L.map('mapid').setView([50.621945, 26.249314], 15);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var  chooseMaker = function(color) {
  var markerUrl;

  switch(color) {
    case "green": 
      markerUrl = 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png';
      break;
    case "blue": 
      markerUrl = 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png';
      break;
    case "red": 
      markerUrl = 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png';
      break;
    default:
      markerUrl = 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png';
    }

    return new L.Icon({
      iconUrl: markerUrl,
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
};

var markersId = {};
var markerColor;
var markers = L.markerClusterGroup();

Object.keys(jsonData).forEach(function(key) {

  var issue = jsonData[key];

  switch(issue.fields.category) {
    case 1: 
      markerColor = chooseMaker("red");
      break;
    case 2: 
      markerColor = chooseMaker("green");
      break;
    case 3: 
      markerColor = chooseMaker("blue");
      break;
    default:
      markerColor = chooseMaker();
  }

  markersId[issue.pk] = L.marker([issue.fields.locationX,
      issue.fields.locationY],{icon: markerColor}).addTo(map);

  markersId[issue.pk]._icon.id = "issue_" + issue.pk;
  markers.addLayer(markersId[issue.pk]);
});


map.addLayer(markers);

var issue_box = document.getElementById("issue_description");

document.addEventListener('click', function(event){
  event.preventDefault();
  if (event.target.id.slice(0,6) == "issue_") {
    callId(event.target.id.slice(6));
  }
  
});

function callId(issue_id) {
  var xml = new XMLHttpRequest();
  xml.open("GET", "getissuebyid/" + issue_id, true);
  xml.send();
  xml.onload = function(){
    var response = JSON.parse(xml.responseText);
    issue_box.style.display = 'block';
    issue_box.innerHTML = response;
  };
}

})();

