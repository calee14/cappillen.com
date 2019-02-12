console.log("Hello World");
$("#about-button").click(function() {
    $('html, body').animate({
        scrollTop: $("#about").offset().top
    }, 2000);
});
$("#projects-button").click(function() {
    $('html, body').animate({
        scrollTop: $("#projects").offset().top
    }, 2000);
});