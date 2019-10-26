let spinner = $("#spinner");
let spinnerWrapper = $("#spinner-wrapper");

// start loader
loadUntilDocument();

// start specific loader
/*
if(window.location.pathname !== "/articles/All/"){
    loadUntilDocument();
}
*/

function loadUntilDocument(){
    spinnerWrapper.addClass('active');
    $("body").css({"overflow": "hidden"});

    $(function(){
        setTimeout(function () {
            spinnerWrapper.removeClass('active');
            $("body").css({"overflow": "visible"});
        }, 400);
    })
}
