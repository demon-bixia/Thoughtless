$(function () {

    let dropdown = $('.dropdown-list');
    dropdown.hover(function () {
            $(this).children('.submenu').fadeIn();
        },

        function () {
            $(this).children('.submenu').fadeOut();
        });

    let button = $('#nav-menu li a.button');
    button.hover(
        function () {
            $(this).css({'background': '#6773f1', 'color': '#fff'})
        },
        function () {
            $(this).css({'background': 'transparent', 'color': '#959faa'})
        });

    $(window).scroll(function () {
        if (pageYOffset >= 90) {
            $('#nav-bar').addClass('shadow-on');
            $('#nav-menu li a.button').css({'background': '#000', "color": '#fff'})
        } else {
            $('#nav-bar').removeClass('shadow-on');
            $('#nav-menu li a.button').css({'background': 'transparent', "color": '#959faa'})
        }
    });
});