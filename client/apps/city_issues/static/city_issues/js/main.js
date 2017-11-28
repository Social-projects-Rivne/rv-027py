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


  IssueMap.prototype.iconCreate = function(category) {
    return new L.Icon({
      iconUrl: '/static/city_issues/img/category_' + category + '_marker-icon.png',
      shadowUrl: '/static/city_issues/img/marker-shadow.png',
      iconSize: [41, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
  };

  IssueMap.prototype.insertAllMarkers = function(jsonData) {
    var markersId = {};

    jsonData.forEach(function(key) {
      var issue = JSON.parse(key);

    markersId[issue.pk] = L.marker([issue.fields.location_lat,
        issue.fields.location_lon],{icon: current.iconCreate(issue.fields.category)}).addTo(current.getMap());

    markersId[issue.pk]._icon.id = "issue_primary-id" + issue.pk;

    });


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
    document.querySelector(".issue_title").innerHTML = jsonData.title;
    document.querySelector(".issue_description").innerHTML = jsonData.description;
    var imgBox = document.querySelector(".issue_img-box");
    imgBox.innerHTML = "";
    if (jsonData.images_urls.length > 0) {
      insertTemplateForBootstrapCarousel("#issue_img-box", "#bootstrap_carousel");
      bootstrapCarousel(jsonData.images_urls);
    } else {
      var img = document.createElement('img');
      img.src = "/static/city_issues/img/no-image.png";
      img.classList.add("issue_img");
      imgBox.appendChild(img);
    }
    var dataUrl =  document.getElementById("issue_edit").getAttribute("data-url").slice(0,-1);
    document.getElementById("issue_edit").setAttribute("href", dataUrl + jsonData.id);

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

function bootstrapCarousel(images_urls) {
  var media = "/media/";
  $(document).ready(function(){  
  for(var i=0 ; i< images_urls.length ; i++) {
    $('<div class="item"><img src="'+media+images_urls[i]+'"><div class="carousel-caption"></div>   </div>').appendTo('.carousel-inner');
    $('<li data-target="#carousel-example-generic" data-slide-to="'+i+'"></li>').appendTo('.carousel-indicators');
  }
  $('.item').first().addClass('active');
  $('.carousel-indicators > li').first().addClass('active');
  $('#carousel-example-generic').carousel();
});
}


function insertTemplateForBootstrapCarousel(parentId, templateId) {
  if ('content' in document.createElement('template')) {
    var template = document.querySelector(templateId);
    var parent = document.querySelector(parentId);
    var clone = document.importNode(template.content, true);
    parent.appendChild(clone);
  }
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

