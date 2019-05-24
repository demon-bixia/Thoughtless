$(function(){
    let username = $("#id_username");
    let password = $("#id_password");

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
             error.html("")
             }
         }
    });
});