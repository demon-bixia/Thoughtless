$(function (e) {
    let inputField = $('#search-modal .input-group-field');

    inputField.on('focus', changeIcon);
    inputField.on('input', changeIcon);

    function changeIcon(e){
        let BackspaceIcon = $("#search-modal .input-group").find('.backspace-icon i');

        if(inputField.val()){
            BackspaceIcon.addClass('fa fa-backspace');
        }else if(BackspaceIcon.hasClass('fa fa-backspace')){
            BackspaceIcon.removeClass('fa fa-backspace');
        }
    }
});