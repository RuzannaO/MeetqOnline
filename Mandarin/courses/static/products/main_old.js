$(document).ready(function () {
  $(".courses-owl-carousel").owlCarousel({
    autoPlay: 5000,
    items: 4,
    itemsDesktop: [1199, 3],
    itemsDesktopSmall: [979, 3],
    center: true,
    nav: true,
    loop: true,
    responsive: {
      600: {
        items: 4,
      },
    },
    navigation: true,
    navigationText: [
      "<i class='fa fa-chevron-left'></i>",
      "<i class='fa fa-chevron-right'></i>",
    ],
  });
  $(".course-owl-carousel").owlCarousel({
    autoPlay: false,
    items: 5,
  margin: 10,
    itemsDesktop: [1199, 3],
    itemsDesktopSmall: [979, 3],
    center: true,
    nav: true,
    loop: true,
    responsive: {
      600: {
        items: 5,
      },
    },
    navigation: true,
    navigationText: [
      "<i class='fa fa-chevron-left'></i>",
      "<i class='fa fa-chevron-right'></i>",
    ],
  });
   $(".course-detail-owl-carousel").owlCarousel({
    autoPlay: false,
    items: 4,
    itemsDesktop: [1199, 3],
    itemsDesktopSmall: [979, 3],
    center: true,
    nav: true,
    loop: true,
    responsive: {
      600: {
        items: 4,
      },
    },
    navigation: true,
    navigationText: [
      "<i class='fa fa-chevron-left'></i>",
      "<i class='fa fa-chevron-right'></i>",
    ],
  });

  $("#showDescription").click(function () {
    $(".show").removeClass("show");
    $("#collapse2").addClass("show");
  });
});

$(".carousel").carousel();
