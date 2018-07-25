$(document).ready(function(){
    $("#fridge-open").click(function(){
        $("#fridge-open").toggle();
        $("#fridge").toggle();
    });
})

$(document).ready(function(){
    $("#close").click(function(){
        $("#fridge").toggle();
        $("#fridge-open").toggle();
    });
})