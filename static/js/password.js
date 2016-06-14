
function stopRKey(evt) {
    var evt = (evt) ? evt : ((event) ? event : null);
    var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
    if ((evt.keyCode == 13) && (node.type=="text")) {return false;}
}

function onclick_btnSubmit(e){
    var form = document.getElementById('fromlogin');
    form.submit();
}

function reqListener(e){
    data = JSON.parse(e.target.responseText);
    imgitems = document.getElementById('imgitems');
    
    imgitems.innerHTML = "";
    data.passwords.forEach(function(index){
        var imgLoad = "\
        <div class='item'>\
        <label>\
        <input type='radio' name='password' value='" + index + "' required='true'>\
        <img src='/media/" + index + "' alt='" + index + "' style='height: 100px; width: 120px'>\
        </label>\
        </div>";
        
        imgitems.innerHTML += imgLoad;
    });
}

function onkeypress_txtUsername(e){
    if (e.keyCode != 13)
        return;
    
    var username = document.getElementById('txtUsername').value;
    
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", '/passwords?username=' + username, true);
    xhttp.addEventListener("load", reqListener);
    xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhttp.send()
}

window.onload = function() {
    document.onkeypress = stopRKey; 

    var btnSubmit = document.getElementById('btnSubmit');
    btnSubmit.addEventListener('click', onclick_btnSubmit);
    
    var txtUsername = document.getElementById('txtUsername');
    txtUsername.addEventListener('keypress', onkeypress_txtUsername);
}

