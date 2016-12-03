function addElement(){
        var xhr = new XMLHttpRequest();
        var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        xhr.open('POST', '../addElement/', true);
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
        var body = new Object();
        if (correct) {
                body.geom = input;
                body.correct = 1;
        } else {
                body.correct = 0;
        }
        body.sidewalks = JSON.stringify(sidewalkData);
        body.intersection = intersection_id;
        xhr.send(JSON.stringify(body));
}

function deleteElement(){
        var xhr = new XMLHttpRequest();
        var csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
        xhr.open('POST', '../deleteElement/', true);
        xhr.setRequestHeader("X-CSRFToken", csrf_token);
        xhr.setRequestHeader('intersection', intersection_id);
        xhr.send(input);
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
        var sidewalksStyle = {"color": "#7cf5ff"};
        sidewalks.addTo(map);

        // bbox for selected area
        var bbox = map.getBounds().toBBoxString();
        var apiUrl = 'https://accessmapseattle.com/api/v2/sidewalks.geojson?bbox=';

        // Make the request (jQuery for simplicity)
        var req = $.get(apiUrl + bbox);
        req.done(function (data) {
        // When the data comes back, update the sidewalks layer
            sidewalks.addData(data);
            sidewalkData = sidewalks.toGeoJSON();
            sidewalks.setStyle(sidewalksStyle);
        });

}
