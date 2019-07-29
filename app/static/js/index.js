$(document).ready(function() {
  $("#enter").click(function(e) {
    $("#section-web-home").hide();
    $("#section-web-home").removeClass("section");
    $("#home-nav").css("opacity", 1);
    $(".section").addClass("active");
    $(".nav-link").first().addClass("active");
  });

  $("#home-link").click(function(e) {
    e.preventDefault();
    $("body,html").animate(
      {
        scrollTop: $(".section").first().offset().top
      },
      800 //speed
    );
    $(".nav-link.active").removeClass("active");
    $(".nav-link").first().addClass("active");
  });

  $(".nav-link").click(function(e) {
    var targetId = e.target.id.split("-"),
    linkId = targetId[targetId.length - 1];
    $(".nav-link.active").removeClass("active");
    $("body,html").animate(
      {
        scrollTop: $("#section-" + linkId).offset().top
      },
      800 //speed
    );
    $(this).addClass("active");
  });
});
