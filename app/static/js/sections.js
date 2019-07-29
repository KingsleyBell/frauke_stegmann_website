var deleteImageUrl,
  shiftImageUrl,
  shiftSectionUrl;

$(document).ready(function() {
  $(".shift-section-down").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: shiftSectionUrl,
      data: {"section_id": sectionId, "shift": 1},
      success: function(response) {
        if (response.success === true) {
          var section = $("#section-" + sectionId),
            nextSection = section.next('.card');
          $(section).hide().before(nextSection).slideToggle("slow");
        }
      }
    });
  });

  $(".shift-section-up").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: shiftSectionUrl,
      data: {"section_id": sectionId, "shift": -1},
      success: function(response) {
        if (response.success === true) {
          var section = $("#section-" + sectionId),
            previousSection = section.prev('.card');
          $(section).hide().after(previousSection).slideToggle("slow");
        }
      }
    });
  });

  $(".shift-image-down").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 2],
    imageId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: shiftImageUrl,
      data: {"section_id": sectionId, "image_id": imageId, "shift": 1},
      success: function(response) {
        if (response.success === true) {
          var image = $("#image-" + imageId),
            nextImage = image.next('.section-image');
          $(image).hide().before(nextImage).slideToggle("slow");
        }
      }
    });
  });

  $(".shift-image-up").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 2],
    imageId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: shiftImageUrl,
      data: {"section_id": sectionId, "image_id": imageId, "shift": -1},
      success: function(response) {
        if (response.success === true) {
          var image = $("#image-" + imageId),
            previousImage = image.prev('.section-image');
          $(image).hide().after(previousImage).slideToggle("slow");
        }
      }
    });
  });

  $(".delete-section").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      data: {"section_id": sectionId},
      success: function() {
        $("#section-" + sectionId).remove();
      }
    });
  });

  $(".delete-image").click(function(e) {
    var targetId = e.target.id.split('-'),
    sectionId = targetId[targetId.length - 2],
    imageId = targetId[targetId.length - 1];
    $.ajax({
      type: "POST",
      url: deleteImageUrl,
      data: {"image_id": imageId, "section_id": sectionId},
      success: function() {
        $("#image-" + imageId).remove();
      }
    });
  });
});
