(function(){

function IssueMap(elementId) {
  var current = this;
  this.map = L.map(elementId);
  this.issueDescriptionBox = new IssueDescription(this, "mapid", "issue_container", "issue_close");
  this.issueDescriptionBox.addHandler();
  this.currentMarker = undefined;
  this.markers = undefined;
  this.statusRawArr = [
      document.querySelector("#id_show_closed"),
      document.querySelector("#id_show_open"),
      document.querySelector("#id_show_new"),
      document.querySelector("#id_show_on_moderation"),
      document.querySelector("#id_show_deleted"),
      document.querySelector("#id_show_pending_close")
    ];

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


  IssueMap.prototype.iconCreate = function(category, status) {
    var underscoredStatusShadow = '/static/city_issues/img/status_' + status.replace(/ /g, '_') + '.png';
    if (status == "open") {
      underscoredStatusShadow = "/static/city_issues/img/marker-shadow.png";
    }
    var MarkerIcon = L.Icon.extend({
    options: {
        customId: "",
        customStatus: "",
        iconUrl: '/static/city_issues/img/category_' + category + '_marker-icon.png',
        shadowUrl: underscoredStatusShadow,
        iconSize: [30, 30],
        iconAnchor: [5, 35],
        popupAnchor: [1, -34],
        shadowSize: [40, 40],
        shadowAnchor: [10, 40],
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
      var underscoredStatus = '/static/city_issues/img/status_' + issue.fields.status.replace(/ /g, '_') + '.png';
      if (issue.fields.status == "open") {
        underscoredStatus = "/static/city_issues/img/marker-shadow.png";
      }
      var marker = L.marker(
        [issue.fields.location_lat, issue.fields.location_lon],
        {icon: current.iconCreate(issue.fields.category, issue.fields.status),
         title: issue.fields.title,
         customId: issue.pk,
         customStatus: underscoredStatus,
       });

      marker.on("click", function(event){
        current.showIssueDetails(this.options.customId, event);
        if (!current.currentMarker) {
          current.currentMarker = this;
          }

        if (this !== current.currentMarker) {
            if (current.currentMarker._shadow !== null) {
                current.currentMarker._shadow.src = current.currentMarker.options.customStatus;
            }
            current.currentMarker = this;
          }
        
        this._shadow.src ='/static/city_issues/img/icon_active.png';
        current.issueDescriptionBox.loadCurrentMarkerObject(this);
      });

      current.markers.addLayer(marker);
      current.map.addLayer(current.markers);
    });


  };

  IssueMap.prototype.filterHandler = function(event) {
    if (event) {
      event.preventDefault();
    }
    var dateFromValue = document.querySelector("#id_date_from").value;
    var dateToValue = document.querySelector("#id_date_to").value;
    var statusArr = [];
    var filterToSetChecked = localStorage.getItem('updateStatus');

    current.statusRawArr.forEach(function(element) {
      var elementName = (element) ? element.name.slice(5).replace(/_/g, " ") : undefined;

      if (element && filterToSetChecked && elementName == filterToSetChecked) {
        localStorage.removeItem('updateStatus');
        element.checked = true;
      }

      if (element && element.checked ) {
        statusArr.push(elementName);
      }
    });

    var categoryValue = document.querySelector("#id_category").value;
    var searchValue = document.querySelector("#id_search").value;
     
    document.querySelector("#message_box").style.display = "none";
    current.getMarkers(
      "getissuesall/?" +
      "filter=" + "True" + "&" +
      "date_from=" + dateFromValue + "&" + 
      "date_to=" + dateToValue + "&" + 
      "status_arr=" + statusArr + "&" + 
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


function IssueDescription(mapObject, mapId, issueContainerId, issueCloseId) {
  var current = this;
  this.mapObject = mapObject;
  this.mapId = mapId;
  this.issueContainerId = issueContainerId;
  this.issueCloseId = issueCloseId;
  this.issue_box = document.getElementById(issueContainerId);
  this.actionButtons = {
    'open' : document.querySelector(".issue_action[data-action=open]"),
    'edit' : document.querySelector("#issue_action-edit"),
    'pending close' : document.querySelector(".issue_action[data-action='pending close']"),
    'closed' : document.querySelector(".issue_action[data-action=closed]"),
    'deleted' : document.querySelector(".issue_action[data-action=deleted]"),
  };
  this.commentStatusButtons = ((document.querySelector("#issue_comments-form")) ? 
  {
    'public' : document.querySelector("#id_status_0").parentElement,
    'private' : document.querySelector("#id_status_1").parentElement,
    'internal' : document.querySelector("#id_status_2").parentElement,
  } : undefined);

  IssueDescription.prototype.loadCurrentMarkerObject = function(obj) {
    current.markerObject = obj;
  };

  IssueDescription.prototype.removeActionsElements = function(dict) {
    if (dict) {
      for (var key in dict) {
        dict[key].style.display = "none";
      }
    }

  };

  IssueDescription.prototype.listenActionsButtons = function(event){
    if (event.target.dataset.target == "#action_modal") {
      current.issueId = event.target.getAttribute("data-id");
      current.issueAction = event.target.getAttribute("data-action");
    }
  };

  IssueDescription.prototype.paintCommnetsInput = function() {
    if(document.querySelector('#id_status')) {
      var checkedElement = document.querySelector('#id_status input:checked');
      var commentsInput = document.querySelector('.issue_comments-form textarea');
      if (commentsInput.classList.length > 0) {
        commentsInput.classList.forEach(function(className) {
          if (className.indexOf('textarea--') !== -1) {
            commentsInput.classList.remove(className);
          }
        });
      }
    commentsInput.classList.add("textarea--" + checkedElement.value);
    }
  };

  IssueDescription.prototype.sendActionData = function(event) {
    event.preventDefault();
    $('#action_modal').modal('hide');
    localStorage.setItem('updateStatus', current.issueAction);
    var csrf = document.querySelector("#form_action input[name=csrfmiddlewaretoken]").value;
    var formData = new FormData();
    formData.append("action", current.issueAction);
    formData.append("issue_id", current.issueId);
    formData.append("csrfmiddlewaretoken", csrf);
    current.issue_box.style.display = "none";
    current.sendAction(formData, current.issueId);
  };

  IssueDescription.prototype.closeHandler = function(event) {
    if (event.target.id == current.issueCloseId || (event.target.id == "mapid" && current.issue_box.style.display == "block")) {
      current.issue_box.style.display = "none";


      if (current.markerObject._shadow) {
            current.markerObject._shadow.src = current.markerObject.options.customStatus;
          }
    }
  };


  IssueDescription.prototype.insertComments = function(jsonData, key) {
    var commentsList = document.querySelector("#issue_comments");
    commentsList.innerHTML = "";
    for (var i = 0; i < jsonData.length; i++) {
      var item = key ? jsonData[i] : JSON.parse(jsonData[i]);
      var commentBox = document.createElement('li');
      var commentHeader = document.createElement('div');
      var commentText = document.createElement('p');
      var commentAuthor = document.createElement('span');

      commentBox.classList.add("issue_comment-box");

      commentHeader.classList.add("issue_comment-header");
      commentHeader.appendChild(document.createTextNode(item.date_public.slice(0,16) + " "));

      commentAuthor.appendChild(document.createTextNode(item.user__alias));
      commentAuthor.classList.add("issue_comment-author");

      commentText.appendChild(document.createTextNode(item.comment));
      commentText.classList.add("issue_comment-text");
      commentText.classList.add("issue_comment-text--" + item.status);

      commentHeader.appendChild(commentAuthor);
      commentBox.appendChild(commentHeader);
      commentBox.appendChild(commentText);
      commentsList.appendChild(commentBox);
    }
  };

  IssueDescription.prototype.sendComment = function(data,issue_id) {
    var xml = new XMLHttpRequest();
    xml.open("POST", "/postcomment/" + issue_id + "/");

    xml.onload = function() {
      if (xml.status === 200) {
        var response = JSON.parse(xml.responseText).slice(1,-1).replace(/}, {/g,'}}, {{').split('}, {'); 
        current.insertComments(response);
      }
    };

    xml.send(data);
  };

  IssueDescription.prototype.sendAction = function(data,issue_id) {
    var xml = new XMLHttpRequest();
    xml.open("POST", "/issueaction/" + issue_id + "/");
    xml.onload = function() {
      var response = JSON.parse(xml.responseText);
      if (response.result == "success") {
        current.mapObject.filterHandler();
      }
    };
    xml.send(data);
  };



  IssueDescription.prototype.commentsHandler = function(event) {
    event.preventDefault();
    var comment = document.querySelector("#id_comment").value;
    var commentStatus = document.querySelector("#id_status input:checked").value;
    var csrf = document.querySelector("#issue_comments-form input[name=csrfmiddlewaretoken]").value;
    var issue_id = event.target.getAttribute("data-id");
    if (comment.length > 0) {
      document.querySelector("#id_comment").value = "";
      var formData = new FormData();
      formData.append("comment", comment);
      formData.append("status", commentStatus);
      formData.append("csrfmiddlewaretoken", csrf);
      current.sendComment(formData, issue_id);
    }
  };

  IssueDescription.prototype.addHandler = function() {
    document.addEventListener('click', current.closeHandler);
    if ( document.querySelector("#issue_comments-form-btn")) {
      document.querySelector("#issue_comments-form-btn").addEventListener('click', current.commentsHandler);
    }
    document.querySelector("#issue_buttons-box").addEventListener("click", current.listenActionsButtons);
    document.querySelector("#issue_action-send").addEventListener("click", current.sendActionData);
    if ( document.querySelector("#id_status")) {
      document.querySelector("#id_status").addEventListener('click', current.paintCommnetsInput);
    }
  };


  IssueDescription.prototype.insertIssueData = function(jsonData, issue_id) {
    current.issue_box.style.display = 'block';
    current.removeActionsElements(current.actionButtons);
    jsonData.dict_of_actions.list_of_actions.forEach(function(button) {
      current.actionButtons[button].style.display = "inline-block";
      current.actionButtons[button].style.verticalAlign = "top";
      current.actionButtons[button].setAttribute("data-id", issue_id);
    });

    current.removeActionsElements(current.commentStatusButtons);
    commentsButtonsNumber =  jsonData.dict_of_actions.list_of_comments_statuses.length;
    if (current.commentStatusButtons && commentsButtonsNumber > 1) {
      jsonData.dict_of_actions.list_of_comments_statuses.forEach(function(button) {
        current.commentStatusButtons[button].style.display = "inline-block";
        current.commentStatusButtons[button].style.verticalAlign = "top";
      });      
    } else if (current.commentStatusButtons && commentsButtonsNumber === 1) {
      button = jsonData.dict_of_actions.list_of_comments_statuses[0];
        current.commentStatusButtons[button].type = 'hidden';
        current.commentStatusButtons[button].firstElementChild.checked = true;
    }
    current.paintCommnetsInput();

    if (document.querySelector("#issue_comments-form-btn")) {
      document.querySelector("#issue_comments-form-btn").setAttribute("data-id", issue_id);
    }
    current.insertComments(jsonData.comments, true);

    document.querySelector("#issue_title").innerHTML = jsonData.title;
    document.querySelector(".issue_description").innerHTML = jsonData.description;
    document.querySelector("#issue_category").innerHTML = jsonData.category__category;
    document.querySelector("#issue_status").innerHTML = '';
    document.querySelector("#issue_status").appendChild(document.createTextNode(jsonData.status.charAt(0).toUpperCase() + jsonData.status.slice(1)));
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
    var editBtn = document.getElementById("issue_action-edit");
    var dataUrl =  editBtn.getAttribute("data-url").slice(0,-1);
    editBtn.setAttribute("href", dataUrl + issue_id);
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
    if (fullImgUrl === null) {
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

$(document).ready(function() {
  issueMap = new IssueMap("mapid");
  issueMap.setFilterFromBtn("#issue_filter-form-btn");
  issueMap.setFilterFromCloseBtn("#issue_filter-form-close-btn");
  issueMap.setFilterFromShowBtn("#issue_filter-form-show-btn");
  issueMap.setViewPoint(50.621945, 26.249314, 16);
  issueMap.addMapLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
    19, 
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>');
  issueMap.filterHandler();
  issueMap.addHandler();

  insertTemplate("#message_box", "#message_list");
  placeFilter();
});
})();

