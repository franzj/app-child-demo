
var passwords;

function getEstadistica() {
    var estadistica = document.getElementById('estadistica');
    
    if(estadistica) {
        data = estadistica.firstChild.nextSibling.children;
        
        var count = 0;
        var mayor = 0;
        var menor = parseInt(data[1].children[1].textContent);
        var usuario_max = null;
        var usuario_min = null;
        for(var i=1; i < data.length; i++){
            var temp = data[i];
            var temp_num = parseInt(temp.children[1].textContent);
            
            count += temp_num;
            
            if(temp_num > mayor){
                usuario_max = temp;
                mayor = temp_num;
            }
            
            if(temp_num < menor){
                usuario_min = temp;
                menor = temp_num;
            }
        }
        
        var resultados = document.getElementById('resultados');
        resultados.innerHTML = "<b>Usuario con mayor logeo</b><br><label>Usuario: " + 
            usuario_max.children[0].textContent + " ingresos: " + usuario_max.children[1].textContent +
            "<br></label><br><b>Usuario con menor logeo</b><br><label>Usuario: " + 
            usuario_min.children[0].textContent + " ingresos: " + usuario_min.children[1].textContent +
            "<br></label><br><label><b>Promedio de ingresos: </b>" + parseInt(count/data.length) + "</label>";
    }
}

function onchage_Imgs(index){
    passwords.forEach(function(item){
        cambiar(item, index.target.value);
    });
}

function cambiar(item, id){
    if(item.id == parseInt(id)){
        var target = document.getElementById('imgitems');
         
        target.innerHTML = "";
        item.imgs.forEach(function(i){
        
        var imgLoad = "\
            <div class='item'>\
                <label>\
                <input type='radio' name='img_id' value='" + i.id + "' required='true'>\
                <img src='/media/" + i.src + "' alt='" + i.src + "' style='height: 100px; width: 120px'>\
                </label>\
            </div>";

            target.innerHTML += imgLoad;
        });
    }
}

function onchange_accion(e){
    document.getElementById('enviar').disabled = false;
    
    if(e.target.value == "guardar"){
        document.getElementById('ddlPasswords').disabled = true;
        document.getElementById('fileupload').disabled = false;
        document.getElementById('pass_id').disabled = false;
        
        document.getElementById('imgitems').innerHTML = "";
    } 
    else {
        document.getElementById('fileupload').disabled = true;
        document.getElementById('pass_id').disabled = true;
        
        var pass =  document.getElementById('ddlPasswords');
        pass.disabled = false;
        
        passwords.forEach(function(item){
            cambiar(item, pass.children[0].value);
        });
    }
}

function onclick_enviar(e){
    var form = document.getElementById('formulario');
    form.submit();
}

window.onload = function() {
    getEstadistica();
    
    var oReq = new XMLHttpRequest();
    oReq.addEventListener("load", function(){
        var pass = document.getElementById("ddlPasswords");
        var pass_up = document.getElementById("pass_id");
        pass.onchange = onchage_Imgs;
        
        data = JSON.parse(this.responseText);
        passwords = data.passwords;
        
        data.passwords.forEach( function(item){
            var liPassword = "<option value='" + item.id +
                "'>" + item.name + "</option>";

            pass.innerHTML += liPassword;
            pass_up.innerHTML += liPassword;
        });
        
        document.getElementById('enviar').onclick = onclick_enviar;
    });
    oReq.open("GET", "/passwords");
    oReq.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    oReq.send();
    
    var accion = document.getElementsByName("accion");
    
    for(var i=0; i< accion.length; i++){
        accion[i].onchange = onchange_accion;
    }
    
    document.getElementById('ddlPasswords').disabled = true;
    document.getElementById('fileupload').disabled = true;
    document.getElementById('enviar').disabled = true;
    document.getElementById('pass_id').disabled = true;
}
