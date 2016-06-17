
var height = 368;
var width = 736;

var x = 368;
var y = 184;
var pelota_id = null;
var disponible = true;
var ctx;
var raf;

var img = new Image();
img.src = '/static/imgs/pelota1.png';

function onchange_pelota(e){
    switch(parseInt(e.target.value)){
        case 1: {
            pelota_id = 1;
            break;      
        }
        case 2: {
            pelota_id = 2;
            break;
        }
        case 3: {
            pelota_id = 3;
            break;
        }
        case 4: {
            pelota_id = 4;
            break;
        }
        default: {
            pelota_id = null;
            break;
        }
    }
}

function onclick_btnIzquierda(e){
    if(disponible && x > 10){
        x -= 10;
    }
}

function onclick_btnArriva(e){
    if(disponible && y > 10){
        y -= 10;
    }
}

function onclick_btnAbajo(e){
    if(disponible && y < 328){
        y += 10;
    }
}

function onclick_btnDerecha(e){
    if(disponible && x < 706){
        x += 10;
    }
}

function onkeydown_cambio(e){
    switch(e.keyCode){
        case 38: {
            onclick_btnArriva(e);
            break;
        }
        case 40: {
            onclick_btnAbajo(e);
            break;
        }
        case 39: {
            onclick_btnDerecha(e);
            break;
        }
        case 37: {
            onclick_btnIzquierda(e);
            break;
        }
        default: {
            break;
        }
    }
}

function cambioPelota(e){
    img.src = '/static/imgs/pelota' + e.target.value + '.png';
}

function idayvuelta(e){
    disponible = false;
        
}

function cuadrilatero(e){

}

function triangulo(e){

}

var ball = {
  x: 100,
  y: 100,
  color: 'blue',
  draw: function() {
    ctx.drawImage(img, x, y);
  }
};

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ball.draw();
  raf = window.requestAnimationFrame(draw);
}

function init(){
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    draw();
}

window.onload = function(){
    var pelotas = document.getElementsByName('pelota');
    
    for(var i=0; i<pelotas.length; i++){
        pelotas[i].onchange = onchange_pelota;
    }
    
    document.getElementById('izquierda').onclick = onclick_btnIzquierda;
    document.getElementById('derecha').onclick = onclick_btnDerecha;
    document.getElementById('arriva').onclick = onclick_btnArriva;    
    document.getElementById('abajo').onclick = onclick_btnAbajo;
    
    init()
    
    document.onkeydown  = onkeydown_cambio;
    
    document.getElementById('idayvuelta').onclick = idayvuelta;
    document.getElementById('cuadrilatero').onclick = cuadrilatero;
    document.getElementById('triangulo').onclick = triangulo;
    
    pelota = document.getElementsByName('pelota');
    for(var i=0; i<pelota.length;i++){
        pelota[i].onchange = cambioPelota;
    }
}
