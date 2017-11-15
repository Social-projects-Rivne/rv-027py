var map = L.map('mapid').setView([50.621945, 26.249314], 15);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var greenIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var redIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var blueIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var markersId = {}
var markers = L.markerClusterGroup();
var markerColor

Object.keys(jsonData).forEach(function(key) {
	switch(jsonData[key].fields.category) {
		case 1: 
			markerColor = redIcon;
			break;
		case 2: 
			markerColor = greenIcon;
			break;
		case 3: 
			markerColor = blueIcon;
			break;
		default:
			markerColor = blueIcon;
	}

	markersId[jsonData[key].pk] = L.marker([jsonData[key].fields.locationX,
	    jsonData[key].fields.locationY],{icon: markerColor}).addTo(map).bindPopup(jsonData[key].fields.description);

    markersId[jsonData[key].pk]._icon.id = "issue_" + jsonData[key].pk;
    markers.addLayer(markersId[jsonData[key].pk]);
});

map.addLayer(markers);