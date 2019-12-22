let spinner = $(".spinner");
let spinnerWrapper = $(".spinner-wrapper");

// start loader
loadUntilDocument();

function loadUntilDocument(){
    startLoad();

    $(function(){
        setTimeout(endLoad, 400);
    })
}

function startLoad(){
    spinnerWrapper.addClass('active');
    $("body").css({"overflow": "hidden"});
}

function endLoad(){
    spinnerWrapper.removeClass('active');
    $("body").css({"overflow": "visible"});
}
