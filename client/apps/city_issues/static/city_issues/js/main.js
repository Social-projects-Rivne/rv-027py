(function(){

function IssueMap(elementId) {
  var current = this;
  this.map = L.map(elementId);
  this.issueDescriptionBox = new IssueDescription("mapid", "issue_container", "issue_close");
  this.issueDescriptionBox.addHandler();

  IssueMap.prototype.setFilterFromBtn = function(filterFormBtnId) {
    current.filterFormBtn = document.querySelector(filterFormBtnId);
  };

  IssueMap.prototype.setFilterFromCloseBtn = function(filterFormCloseBtnId) {
    current.filterFormCloseBtnId = document.querySelector(filterFormCloseBtnId);
  };

  IssueMap.prototype.setFilterFromShowBtn = function(filterFormShowBtnId) {
    current.filterFormShowBtnId = document.querySelector(filterFormShowBtnId);
  };
   
  
  IssueMap.prototype.setViewPoint = function(latitude, longitude, scale) {
    if (localStorage.getItem('lat') && localStorage.getItem('lng')) {
       this.map.setView([localStorage.getItem('lat'), localStorage.getItem('lng')], scale);
    } else {
      this.map.setView([latitude, longitude], scale);
    }
    
  };


  IssueMap.prototype.addMapLayer = function(mapLink, mapZoom, mapAttribute) {
    L.tileLayer(mapLink, {maxZoom: mapZoom, attribution: mapAttribute}).addTo(this.map);
  };


  IssueMap.prototype.iconCreate = function(category) {
    var MarkerIcon = L.Icon.extend({
    options: {
        customId: "",
        iconUrl: '/static/city_issues/img/category_' + category + '_marker-icon.png',
        shadowUrl: '/static/city_issues/img/marker-shadow.png',
        iconSize: [30, 30],
        iconAnchor: [8, 30],
        popupAnchor: [1, -34],
        shadowSize: [30, 30]
    }});

    return new MarkerIcon();
  };

  IssueMap.prototype.showIssueDetails = function(issueId, event) {
    localStorage.setItem('lat', event.latlng.lat);
    localStorage.setItem('lng', event.latlng.lng);
    current.issueDescriptionBox.getIssueById(issueId);
  };

  IssueMap.prototype.insertAllMarkers = function(jsonData) {
    if (current.markers) {
      current.map.removeLayer(current.markers);
    }

    current.markers = L.markerClusterGroup();
    
    jsonData.forEach(function(key) {
      var issue = JSON.parse(key);
      var marker = L.marker(
        [issue.fields.location_lat, issue.fields.location_lon],
        {icon: current.iconCreate(issue.fields.category),
         title: issue.fields.title,
         customId: issue.pk,
       });

      marker.on("click", function(event){
        current.showIssueDetails(this.options.customId, event);
      });

      current.markers.addLayer(marker);
      current.map.addLayer(current.markers);
    });


  };

  IssueMap.prototype.filterHandler = function(event) {
    event.preventDefault();
    var dateFromValue = document.querySelector("#id_date_from").value;
    var dateToValue = document.querySelector("#id_date_to").value;
    var showClosedValue = document.querySelector("#id_show_closed").checked;
    var categoryValue = document.querySelector("#id_category").value;
    var searchValue = document.querySelector("#id_search").value;
     
    document.querySelector("#message_box").style.display = "none";
    current.getMarkers(
      "getissuesall/?" +
      "filter=" + "True" + "&" +
      "date_from=" + dateFromValue + "&" + 
      "date_to=" + dateToValue + "&" + 
      "show_closed=" + showClosedValue + "&" + 
      "category=" + categoryValue + "&" +
      "search=" +  searchValue
      );
    
  };


  IssueMap.prototype.filterCloseHandler = function(event) {
    document.querySelector("#issue_form-container").style.display = "none";
    current.filterFormShowBtnId.style.display = "block";
  };

  IssueMap.prototype.filterShowHandler = function(event) {
    document.querySelector("#issue_form-container").style.display = "block";
    current.filterFormShowBtnId.style.display = "none";
  };

  IssueMap.prototype.addHandler = function() {
    current.filterFormBtn.addEventListener('click', current.filterHandler);
    current.filterFormCloseBtnId.addEventListener('click', current.filterCloseHandler);
    current.filterFormShowBtnId.addEventListener('click', current.filterShowHandler);
  };

  IssueMap.prototype.getMarkers = function(serverURL) {
    var xml = new XMLHttpRequest();
    xml.open("GET", serverURL, true);
    xml.send();
    xml.onload = function(){
      if (xml.responseText == "\"[]\"") {
        if (current.markers) {
          current.map.removeLayer(current.markers);
        }
        document.querySelector("#message_box").style.display = "block";
        document.querySelector("#message_box li").innerHTML = "No data for that filter choice.";
        return;
      }
      document.querySelector("#message_box").style.display = "none";
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

  IssueDescription.prototype.closeIssueDescriptionHandler = function(event) {
      if (event.target.id == "mapid" && current.issue_box.style.display == "block") {
        current.issue_box.style.display = 'none';
      }
  };

  IssueDescription.prototype.closeHandler = function(event) {
    if (event.target.id == current.issueCloseId) {
      current.issue_box.style.display = "none";
    }
  };

  IssueDescription.prototype.addHandler = function() {
    document.addEventListener('click', current.closeIssueDescriptionHandler);
    document.addEventListener('click', current.closeHandler);
  };


  IssueDescription.prototype.insertIssueData = function(jsonData, issue_id) {
    current.issue_box.style.display = 'block';
    document.querySelector(".issue_title").innerHTML = jsonData.title;
    document.querySelector(".issue_description").innerHTML = jsonData.description;
    document.querySelector("#issue_category").innerHTML = jsonData.category__category;
    var imgBox = document.querySelector(".issue_img-box");
    imgBox.innerHTML = "";
    if (jsonData.images_urls.length > 0) {
      insertTemplate("#issue_img-box", "#bootstrap_carousel");
      bootstrapCarousel(jsonData.images_urls);
    } else {
      var img = document.createElement('img');
      img.src = "/static/city_issues/img/no-image.png";
      img.classList.add("issue_img");
      imgBox.appendChild(img);
    }
    var editBtn = document.getElementById("issue_edit");
    var dataUrl =  editBtn.getAttribute("data-url").slice(0,-1);
    editBtn.setAttribute("href", dataUrl + issue_id);
    editBtn.style.display = "none";
    if (jsonData.editable) {
      editBtn.style.display = "inline-block";
    }

  };


  IssueDescription.prototype.getIssueById = function(issue_id) {
    var xml = new XMLHttpRequest();
    xml.open("GET", "getissuebyid/" + issue_id, true);
    xml.send();
    xml.onload = function(){
      var response = JSON.parse(JSON.parse(xml.responseText).slice(1,-1));
      current.insertIssueData(response, issue_id);
    };
  };

}

function bootstrapCarousel(images_urls) {
  $(document).ready(function(){  
  for(var i=0 ; i< images_urls.length ; i++) {
    var fullImgUrl = images_urls[i];
    if (fullImgUrl !== null) {
        fullImgUrl = "/media/" + fullImgUrl;
    } else {
        fullImgUrl = "/static/city_issues/img/no-image.png";
    }
    
  $('<div class="item"><img src="' + fullImgUrl + '"><div class="carousel-caption"></div>   </div>').appendTo('.carousel-inner');
  $('<li data-target="#carousel-example-generic" data-slide-to="'+i+'"></li>').appendTo('.carousel-indicators');
  }
  $('.item').first().addClass('active');
  $('.carousel-indicators > li').first().addClass('active');
  $('#carousel-example-generic').carousel();
});
}


function insertTemplate(parentId, templateId) {
  if ('content' in document.createElement('template')) {
    var template = document.querySelector(templateId);
    var parent = document.querySelector(parentId);
    var clone = document.importNode(template.content, true);
    parent.appendChild(clone);
  }
}

function placeFilter() {
  var leafletControls = document.querySelector(".leaflet-top.leaflet-left");
  var filterForm = document.querySelector("#issue_form-box");

  leafletControlsCoordinatse = leafletControls.getBoundingClientRect();
  filterForm.style.top = (leafletControlsCoordinatse.bottom + 5) + "px";
  filterForm.style.left = (leafletControlsCoordinatse.left + 5) + "px";
}


issueMap = new IssueMap("mapid");
issueMap.setFilterFromBtn("#issue_filter-form-btn");
issueMap.setFilterFromCloseBtn("#issue_filter-form-close-btn");
issueMap.setFilterFromShowBtn("#issue_filter-form-show-btn");
issueMap.setViewPoint(50.621945, 26.249314, 16);
issueMap.addMapLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
  19, 
  '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>');
issueMap.getMarkers("getissuesall/");
issueMap.addHandler();

insertTemplate("#message_box", "#message_list");
placeFilter();

})();

