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
        lat = json['coordinates'][1];
        lon = json['coordinates'][0];
        map.setView([lat, lon], 18);
}
