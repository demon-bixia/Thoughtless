$(function(){    let form = $("#form");

    let username = $("#id_username");
    let password = $("#id_password");
    let password_confirm = $("#id_password_confirm");
    let email = $("#id_email");

    username.on("input", function(){
        let error = $(this).siblings('.error-text');
        if ($(this).val() === ""){
            error.html("username is required");
        }
         else{
         if (error.html() !== "") {
             error.html("")
             }
         }

    });

    password.on("input", function(){
        let error = $(this).siblings('.error-text');
        if ($(this).val() === "") {
            error.html("password is required");
        }
        else{
         if (error.html() !== "") {
             error.html("");
             }
         }
    });

    password_confirm.on("change", function(){
        let error = $(this).siblings('.error-text');
        if($(this).val() !== password.val()){
            error.html('Password mismatch');
        }
        else{
             error.html("")
         }
    });

    email.on("change", function(){
        let error = $(this).siblings('.error-text');
        $.ajax({
            url:"/accounts/valid_email/",
            type:"get",
            dataType:"json",
            data: {"email":$(this).val()},
            success: function(data){
                // noinspection JSUnresolvedVariable
                if (data.is_valid){
                    error.html("")
                }else{
                    error.html("this email is taken")
                }
            }
        });
    });

    email.on("input", function(){
        let error = $(this).siblings('.error-text');
        if ($(this).val() === ""){
            error.html("email is required");
        }
        else{
         if (error.html() !== "") {
             error.html("")
             }
         }
    });
});
