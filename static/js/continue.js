
function onchange_departamento(e){
    var target = document.getElementById("provincias");
    var data = ubigeo.provincias[e.target.value]
    
    target.innerHTML = "";
    data.forEach(function(index){
        target.innerHTML += "<option value='" + index.id_ubigeo + 
            "'>" + index.nombre_ubigeo + "</option>";
        
    });
}

window.onload = function(){
    var sdp = document.getElementById("departamentos");
    var spv = document.getElementById("provincias");
    
    ubigeo.departamentos.forEach(function(index){
        sdp.innerHTML += "<option value='" + index.id_ubigeo + 
            "'>" + index.nombre_ubigeo + "</option>";
        
    });
    
    ubigeo.provincias[ubigeo.departamentos[0].id_ubigeo].forEach(function(index){
        spv.innerHTML += "<option value='" + index.id_ubigeo + 
            "'>" + index.nombre_ubigeo + "</option>";
    });
    
    sdp.onchange = onchange_departamento;
}
