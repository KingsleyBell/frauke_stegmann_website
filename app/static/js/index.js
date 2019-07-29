$(document).ready(function() {
  $("#enter").click(function(e) {
    $("#section-web-home").hide();
    $("#section-web-home").removeClass("section");
    $("#home-nav").css("opacity", 1);
    $(".section").first().addClass("active");
    $(".nav-link").first().addClass("active");
  });

  $("#home-link").click(function(e) {
    e.preventDefault();
    $(".section.active").removeClass("active");
    $(".nav-link.active").removeClass("active");
    $(".section").first().addClass("active");
    $(".nav-link").first().addClass("active");
  });

  $(".nav-link").click(function(e) {
    var targetId = e.target.id.split("-"),
    linkId = targetId[targetId.length - 1];
    $(".section.active").removeClass("active");
    $(".nav-link.active").removeClass("active");

    $("#section-" + linkId).addClass("active");
    $(this).addClass("active");
  });
});
