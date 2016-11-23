function addElement(json){
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '../addElement/', true);
        xhr.send(json);
}
function deleteElement(json){
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '../deleteElement/', true);
        xhr.send(json);
}
