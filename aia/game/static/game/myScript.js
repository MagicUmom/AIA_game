function myFunction() {
    document.getElementById("demo").innerHTML = "HeyHeyHey";
}

var now_bet_amount = 0;
var bet_red = 0;
var bet_white = 0;
var total_balance = 5000;

function bet_button(elem){
    var value = elem.value;
    if(value>0){
        console.log(value);
        now_bet_amount += Number(value);
        document.getElementById("amount").innerHTML = now_bet_amount;
    }else{
        console.log(value);
        document.getElementById("amount").innerHTML = 0;
        now_bet_amount = 0;
    }

}

function pool_button(elem){
    var id = elem.id;
    if(id == 'pool_red'){
        // console.log(id);
        var red_val = document.getElementById("text_pool_red").innerHTML;
        if (isHaveMoney(Number(now_bet_amount))){
            document.getElementById("text_pool_red").innerHTML = Number(red_val) + now_bet_amount;
            document.getElementById("amount").innerHTML = 0;
            update_balance(now_bet_amount);
            now_bet_amount = 0;
        }

    }else if (id == 'pool_white') {
        // console.log(id);
        var white_val = document.getElementById("text_pool_white").innerHTML;
        if (isHaveMoney(now_bet_amount)){
            document.getElementById("text_pool_white").innerHTML = Number(white_val) + now_bet_amount;
            document.getElementById("amount").innerHTML = 0;
            update_balance(now_bet_amount);
            now_bet_amount = 0;
        }
    }
}

function update_balance(value){
        total_balance = total_balance - value;
        document.getElementById("balance_count").innerHTML = total_balance;
}

function isHaveMoney(value){
    if(total_balance >= value){
        // console.log("isHaveMoney True", total_balance,value);
        return true;
    }else{
        // console.log("isHaveMoney False", total_balance,value);
        return false;
    }
}
