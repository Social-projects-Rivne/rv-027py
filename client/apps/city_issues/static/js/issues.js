function IssueMap()
{
    this.map = L.map('map').locate({setView: true, maxZoom: 50});
    this.layer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(this.map);

    this.map.on('click',($.proxy(this.getLocation, this)));
    this.marker = '';
}

IssueMap.prototype.getLocation = function (e)
{
    if(this.map.hasLayer(this.marker))
        this.map.removeLayer(this.marker);

    var location = e.latlng;
    this.marker = L.marker(location, { draggable: true}).addTo(this.map);

     $("input[name=location_lat]").val(location.lat);
     $("input[name=location_lon]").val(location.lng);
};

$(function ()
{
    new IssueMap();
});
