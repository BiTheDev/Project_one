function changeimg(){
    var num = Math.ceil(Math.random() * 2)
    document.body.background = "static/img/food-"+num+".jpg";
    document.body.style.backgroundSize = "cover";
}

$(document).ready(function(){
    $("#register").click(function(){
        $("#container").toggle();
        $("#wrapper").toggle();
    });
})

$(document).ready(function(){
    $("#back").click(function(){
        $("#container").toggle();
        $("#wrapper").toggle();
    });
})