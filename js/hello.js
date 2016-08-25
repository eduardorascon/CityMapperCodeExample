$(document).ready(function() {
    initMarkers();
    initMap();
});

var map;
function initMap(){
    map = new google.maps.Map(document.getElementById('map'), 
    {
        center: { lat:19.4057, lng:-99.1488 },
        zoom: 13
    });

    google.maps.event.addListener(map, 'click', function(event)
    {
        placeMarker(event.latLng);
    });
}

//Return distance in meters between markers.
function calculateDistance(fromMarker, toMarker)
{
    if(fromMarker ==  null || toMarker == null)
        return;

    return google.maps.geometry.spherical.computeDistanceBetween(fromMarker.getPosition(), toMarker.getPosition());;
};

var nearby_from_start_marker, nearby_from_end_marker;
function displayNearbyMarkers(marker)
{
    //Fist we need to remove older nearby markers.
    hideLastNearbyMarkers(marker);

    //Lest show only 3 markers.
    var max_markers_to_display = 3, markers_counter = 0;
    var nearby_markers = []
    var is_distance_allowed, is_max_markers_reached;
    $.each(station_markers, function(index, data)
    {
        //Check if marker should be shown.
        is_max_markers_reached = markers_counter == max_markers_to_display
        //Exit loop when max_markers_to_display is reached
        if(is_max_markers_reached)
            return true;//jQuery equivalent to 'continue'

        is_distance_allowed = calculateDistance(marker, station_markers[index]) <= 180;
        if(is_distance_allowed)
        {
            markers_counter++;
            station_markers[index].setMap(map);
            nearby_markers.push(station_markers[index]);
        }
    });

    //Check if marker is start_marker or end_marker
    if(marker === start_marker)
        nearby_from_start_marker = nearby_markers;
    else
        nearby_from_end_marker = nearby_markers;

    //Always display markers on top
    marker.setZIndex(google.maps.Marker.MAX_ZINDEX + 1);
}

//Remove close markers from map if there is any.
function hideLastNearbyMarkers(marker)
{
    //Check if marker is start_marker or end_marker
    var markers_to_remove, other_markers;
    if (marker == start_marker)
    {
        markers_to_remove = nearby_from_start_marker;
        other_markers = nearby_from_end_marker;
    }
    else
    {
        markers_to_remove = nearby_from_end_marker;
        other_markers = nearby_from_start_marker;
    }

    if(markers_to_remove == null)
        return;

    //Lets iterate over makers_to_remove and other_markers to check if a marker is shared between them.
    $.each(markers_to_remove, function(markers_index, makers_data)
    {
        var is_marker_unique = true;
        $.each(other_markers, function(other_index, other_data)
        {
            //Check if markers are duplicated.
            if(markers_to_remove[markers_index] == other_markers[other_index])
            {
                is_marker_unique = false;
                return true;//jQuery equivalent to 'continue'
            }
        });

        //Remove marker from map
        if(is_marker_unique == true)
            markers_to_remove[markers_index].setMap(null);
    });

    //Delete every item from array;
    markers_to_remove = [];
}

//Place start or end marker.
var start_marker, end_marker;
function placeMarker(location)
{
    //when start and end marker are set remove 'click' listener from map
    if(end_marker != null){
        google.maps.event.clearListeners(map, 'click');
        return;
    }

    var marker = new google.maps.Marker({
        position: location,
        draggable: true,
        icon: 'http://maps.google.com/mapfiles/ms/icons/' + (start_marker == null ? 'yellow-dot.png' : 'red-dot.png'),
        map: map
    });

    google.maps.event.addListener(marker, 'dragend', function(event)
    {
        displayNearbyMarkers(marker);
    });

    //Set marker as start_marker or end_marker
    if(start_marker == null)
        start_marker = marker;
    else
        end_marker = marker;

    //
    displayNearbyMarkers(marker);
}

var station_markers = [];
var station_positions = [];
function initMarkers () 
{
    $.ajax(
    {
        type:"POST",
        url:"/ecobici",
        dataType: "json"
    })
    .done(function(data) 
    {
        $.each(data["stations"], function(index, data) {
            position = new google.maps.LatLng((data["location"])["lat"], (data["location"])["lon"]);
            station_positions.push(position);
            var marker = new google.maps.Marker(
            {
                position: position,
                icon: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
            });
            station_markers.push(marker);
        });

        //drawEcobiciCoveragePolygon();
        sortPoints2Polygon();
    });
}

function drawEcobiciCoveragePolygon()
{
    var coverage = new google.maps.Polygon(
    {
        //paths: station_markers,
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 3,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map
    });
}

function getPolygonEdges()
{
    var wtc = new google.maps.Marker(
    {
        position: new google.maps.LatLng(19.3895452,-99.1767453)
    });
}

function sortPoints2Polygon() 
{
    points = [];
    var bounds = new google.maps.LatLngBounds(); 
    for (var i=0; i < station_positions.length; i++)
    {
        points.push(station_positions[i]);
        bounds.extend(station_positions[i]);
    }
    var center = bounds.getCenter();
    var bearing = [];
    
    for (var i=0; i < points.length; i++)
        points[i].bearing = google.maps.geometry.spherical.computeHeading(center, points[i]);
        
    points.sort(bearingsort);
    return points;
}

function bearingsort(a,b)
{
    return (a.bearing - b.bearing);
}