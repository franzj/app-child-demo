var passwords;

function onchage_Imgs(index){
    passwords.forEach(function(item){
        if(item.id == parseInt(index.target.value)){
            $("#imgitems").html("");

            item.imgs.forEach(function(i){
                var imgLoad = "\
                <div class='item'>\
                    <label>\
                    <input type='radio' name='password' value='" + i.src + "' required='true'>\
                    <img src='/media/" + i.src + "' alt='" + i.id + "' style='height: 100px; width: 120px'>\
                    </label>\
                </div>";

                content = $("#imgitems");

                htmltext = content.html();
                content.html(htmltext + imgLoad);
            });
        }
    });
}


function onclick_btnVerificar(e) {
    var re = RegExp("^[A-Za-z]+$");
    var nombre = $("#txtUsername").val();

    if (re.test(nombre)){
        $.ajax( "/verificar?nombre=" + nombre ).done(function(data){
            if (data.status == 404) {
                alert(data.mensaje);
            }
            else if (data.status == 302) {
                alert(data.mensaje);
            }
            else {
                console.log("Error del servidor");
            }
        });
    }
    else {
        alert("Solo letras...");
    }
}

$( document ).ready( function () {
    $.ajax( "/passwords" ).done( function(data) {
        var ddi = $( "#ddlPasswords" );

        passwords = data.passwords;

        data.passwords.forEach( function(item){
            var liPassword = "<option value='" + item.id +
                "'>" + item.name + "</option>";

            var stringHtml = ddi.html();

            ddi.html(stringHtml + liPassword);
        });

        $("#btnVerificar").click(onclick_btnVerificar);
        $("#ddlPasswords").change(onchage_Imgs);

        $("#ddlPasswords option:first-child").change()
    });
});
