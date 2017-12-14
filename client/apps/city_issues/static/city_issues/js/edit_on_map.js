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

    this.marker = L.marker([this.lat, this.lng], {draggable: true}).addTo(this.map);


    this.map.on('click', ($.proxy(this.getLocation, this)));
    this.marker.on('dragend', ($.proxy(this.getDragLocation, this)));
    $('a.del-img').on('click', ($.proxy(this.onDeleteImage, this)));

}

IssueMap.prototype.getLocation = function (e) {
    if (this.map.hasLayer(this.marker))
        this.map.removeLayer(this.marker);
    var location = e.latlng;
    this.marker = L.marker(location, {draggable: true}).addTo(this.map);
    this.marker.off('dragend');
    this.marker.on('dragend', ($.proxy(this.getDragLocation, this)));
    $.proxy(this.setInputLocation(location), this);

};

IssueMap.prototype.getDragLocation = function (e) {
    if (this.map.hasLayer(this.marker))
        this.map.removeLayer(this.marker);
    this.marker = e.target;
    var location = this.marker.getLatLng();
    this.marker.setLatLng(location, {draggable: true}).addTo(this.map);
    $.proxy(this.setInputLocation(location), this);
};


IssueMap.prototype.setInputLocation = function (location) {
    $("input[name=location_lat]").val(location.lat);
    $("input[name=location_lon]").val(location.lng);
    localStorage.setItem('lat', location.lat);
    localStorage.setItem('lng', location.lng);
};

IssueMap.prototype.onDeleteImage = function (event) {
    var imageID = $(event.target).attr('data-attach-id');
    $('input[name=attachment-id]').val(imageID);
};

$(function () {
    new IssueMap();
});



