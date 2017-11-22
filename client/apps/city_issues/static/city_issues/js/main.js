(function(){

function IssueMap(elementId) {
  var current = this;
  this.map = L.map(elementId);
  
  IssueMap.prototype.getMap = function() {
    return this.map;
  };

  IssueMap.prototype.setViewPoint = function(latitude, longitude, scale) {
    this.map.setView([latitude, longitude], scale);
  };


  IssueMap.prototype.addMapLayer = function(mapLink, mapZoom, mapAttribute) {
    L.tileLayer(mapLink, {maxZoom: mapZoom, attribution: mapAttribute}).addTo(this.map);
  };

  IssueMap.prototype.chooseMarker = function(color) {
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

  IssueMap.prototype.insertAllMarkers = function(jsonData) {
    var markersId = {};
    var markerColor;
    var markers = L.markerClusterGroup();

    jsonData.forEach(function(key) {
      var issue = JSON.parse(key);

      switch(issue.fields.category) {
        case 1: 
          markerColor = issueMap.chooseMarker("red");
          break;
        case 2: 
          markerColor = issueMap.chooseMarker("green");
          break;
        case 3: 
          markerColor = issueMap.chooseMarker("blue");
          break;
        default:
          markerColor = issueMap.chooseMarker();
      }

    markersId[issue.pk] = L.marker([issue.fields.location_lat,
        issue.fields.location_lon],{icon: markerColor}).addTo(current.getMap());

    markersId[issue.pk]._icon.id = "issue_primary-id" + issue.pk;
    markers.addLayer(markersId[issue.pk]);
    });

    this.getMap().addLayer(markers);
  };

  IssueMap.prototype.getMarkers = function(serverURL) {
    var xml = new XMLHttpRequest();
    xml.open("GET", serverURL, true);
    xml.send();
    xml.onload = function(){
      var response = JSON.parse(xml.responseText).slice(1,-1).replace(/}, {/g,'}}, {{').split('}, {');
      current.insertAllMarkers(response);
    };
  };

}


function IssueDescription(mapId, issueContainerId, issueCloseId) {
  var current = this;
  this.mapId = mapId;
  this.issueContainerId = issueContainerId;
  this.issueCloseId = issueCloseId;
  this.issue_box = document.getElementById(issueContainerId);

  IssueDescription.prototype.markerHandler = function(event) {
    if (event.target.id.slice(0,16) == "issue_primary-id") {
    current.getIssueById(event.target.id.slice(16));
    current.issue_box.style.display = 'block';
      } 
    else {
      if (event.target.id == "mapid" && current.issue_box.style.display == "block") {
        current.issue_box.style.display = 'none';
      }
    }
  };

  IssueDescription.prototype.closeHandler = function(event) {
    if (event.target.id == current.issueCloseId) {
      current.issue_box.style.display = "none";
    }
  };

  IssueDescription.prototype.addHandler = function() {
    document.addEventListener('click', current.markerHandler);
    document.addEventListener('click', current.closeHandler);
  };


  IssueDescription.prototype.insertIssueData = function(jsonData) {
    current.issue_box.style.display = 'block';
    document.querySelector(".issue_name").innerHTML = jsonData.fields.name;
    document.querySelector(".issue_description").innerHTML = jsonData.fields.description;
    var dataUrl =  document.getElementById("issue_edit").getAttribute("data-url").slice(0,-1);
    document.getElementById("issue_edit").setAttribute("href", dataUrl + jsonData.pk);

  };


  IssueDescription.prototype.getIssueById = function(issue_id) {
    var xml = new XMLHttpRequest();
    xml.open("GET", "getissuebyid/" + issue_id, true);
    xml.send();
    xml.onload = function(){
      var response = JSON.parse(JSON.parse(xml.responseText).slice(1,-1));
      current.insertIssueData(response);
    };
  };

}

issueMap = new IssueMap("mapid");
issueMap.setViewPoint(50.621945, 26.249314, 16);
issueMap.addMapLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
  19, 
  '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>');
issueMap.getMarkers("getissuesall/");
issueDescription = new IssueDescription("mapid", "issue_container", "issue_close");
issueDescription.addHandler();
})();

