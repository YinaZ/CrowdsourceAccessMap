function badIntersection(){
        var xhr = new XMLHttpRequest();
        var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        xhr.open('POST', '../badIntersection/', true);
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
        xhr.setRequestHeader('intersection', intersection_id);
        xhr.send();
}

function addElement(json){
        var xhr = new XMLHttpRequest();
        var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        xhr.open('POST', '../addElement/', true);
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
        xhr.setRequestHeader('intersection', intersection_id);
        xhr.send(json);
}
function deleteElement(json){
        var xhr = new XMLHttpRequest();
        var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        xhr.open('POST', '../deleteElement/', true);
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
        xhr.setRequestHeader('intersection', intersection_id);
        xhr.send(json);
}

function getCoordinates() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() { 
            if (xhr.status == 200)
                var jsonResponse = JSON.parse(xhr.responseText);
                changeCoordinates(jsonResponse);
                intersection_id = jsonResponse['id'];
        }
        xhr.open('GET', '../getCoordinates/', true);
        xhr.send();
}

function changeCoordinates(json){
        var lat = json['coordinates'][1];
        var lng = json['coordinates'][0];
        marker.setLatLng([lat, lng]).update();
        map.setView([lat, lng], 18);
        
        // Add a layer for the sidewalks
        var sidewalks = L.geoJson();
        sidewalks.addTo(map);

        // bbox for selected area
        var bbox = map.getBounds().toBBoxString();
        var apiUrl = 'https://accessmapseattle.com/api/v2/sidewalks.geojson?bbox=';

        // Make the request (jQuery for simplicity)
        var req = $.get(apiUrl + bbox);
        req.done(function (data) {
        // When the data comes back, update the sidewalks layer
            sidewalks.addData(data);
            
        });

}
