function IssueMap()
{
    this.map = L.map('map');
    if (localStorage.getItem('lat') && localStorage.getItem('lng')) {
        this.map.setView([localStorage.getItem('lat'), localStorage.getItem('lng')], 15);
    }
    else {
        this.map.locate({setView: true, maxZoom: 50});
    }

    
    this.layer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(this.map);

    this.marker = '';

    this.map.on('click',($.proxy(this.getLocation, this)));
    this.submitBtn = $("#form_submit-btn");
    this.submitBtn.on('click', $.proxy(this.saveLocation, this));
}

IssueMap.prototype.getLocation = function (e)
{
    if(this.map.hasLayer(this.marker))
        this.map.removeLayer(this.marker);

    var location = e.latlng;
    this.marker = L.marker(location, { draggable: true}).addTo(this.map);
    this.marker.off('dragend');
    this.marker.on('dragend', ($.proxy(this.getDragLocation, this)));

     $("input[name=location_lat]").val(location.lat);
     $("input[name=location_lon]").val(location.lng);
};

IssueMap.prototype.getDragLocation = function (e) {
    if (this.map.hasLayer(this.marker))
        this.map.removeLayer(this.marker);
    this.marker = e.target;
    var location = this.marker.getLatLng();
    this.marker.setLatLng(location, {draggable: true}).addTo(this.map);

     $("input[name=location_lat]").val(location.lat);
     $("input[name=location_lon]").val(location.lng);
};


IssueMap.prototype.saveLocation = function (e)
{
    e.preventDefault();
    localStorage.setItem('lat', $("input[name=location_lat]").val());
    localStorage.setItem('lng', $("input[name=location_lon]").val());
    $("#issue_create-form").submit();

};

$(function ()
{
    new IssueMap();
});
