(function(){
    function IssueMap() {
    this.map = L.map('map');
    this.lat = localStorage.getItem('lat');
    this.lng = localStorage.getItem('lng');
    this.scale = 16;

    if (this.lat && this.lng) {
        this.map.setView([this.lat, this.lng], this.scale);
    } else {
        this.map.locate({setView: true, maxZoom: 50});
    }
  
    this.layer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(this.map);

    this.marker = L.marker([this.lat, this.lng], { draggable: false}).addTo(this.map);

    this.map.on('click',($.proxy(this.getLocation, this)));
    
    }

IssueMap.prototype.getLocation = function (e) {
    if(this.map.hasLayer(this.marker))
        this.map.removeLayer(this.marker);
    var location = e.latlng;
    this.marker = L.marker(location, { draggable: false}).addTo(this.map);

     $("input[name=location_lat]").val(location.lat);
     $("input[name=location_lon]").val(location.lng);
     localStorage.setItem('lat', location.lat);
     localStorage.setItem('lng', location.lng);
    };

$(function ()
    {
        new IssueMap();
    });
})();



