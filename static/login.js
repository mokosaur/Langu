$(document).ready(function() {
    var registrationForm = false;
    $("#name-input").hide();
    $("#register").click(function() {
        if(!registrationForm) {
            $('h1').text("Register!");
            $("#name-input").slideDown(100);
            $("#name-input").attr("required", "required");
            $('span').text("You already have an account?");
            $('#register').text("Log in!");
            $('button').text("Register");
            $('form').attr("action", "/register");
        } else {
            $('h1').text("Log in!");
            $("#name-input").slideUp(100);
            $("#name-input").removeAttr("required");
            $('span').text("No account?");
            $('#register').text("Register now!");
            $('button').text("Log in");
            $('form').attr("action", "/login");
        }
        registrationForm = !registrationForm;
    });
});