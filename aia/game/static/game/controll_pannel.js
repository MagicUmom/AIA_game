// global vars;;
var BTN_ON = 0 // 0 : no seleted; 1: red 2:white;

function api_gameover(){
    var request = new XMLHttpRequest();
    request.open('GET', '../admin_api/game_over', true);
    request.send();
    console.log("api_gameover");
}

function api_newgame(){
    var request = new XMLHttpRequest()
    request.open('GET', '../admin_api/new_game', true);
    request.send();
    console.log("api_newgame");
}

function btnred(){
    BTN_ON = 1;
    console.log("api_btnred");
}

function btnwhite(){
    BTN_ON = 2;
    console.log("api_btnwhite");
}

function api_btnconfirm(){
    console.log("api_btnconfirm");
    if(BTN_ON == 1){
        var request = new XMLHttpRequest();
        request.open('GET', '../admin_api/confirm?btn=1', true);
        request.send();
        console.log("BTN_ON = 1");
    }else if(BTN_ON == 2){
        var request = new XMLHttpRequest();
        request.open('GET', '../admin_api/confirm?btn=2', true);
        request.send();
        console.log("BTN_ON = 2");
    }else if(BTN_ON == 0){
        console.log("BTN_ON = 0");
    }
    BTN_ON = 0;
    // TODO:
    // btn clean seleted effect;;
}

function api_btnlock(){
    var request = new XMLHttpRequest();
    request.open('GET', '../admin_api/lock', true);
    request.send();
    console.log("api_btnlock");
}

