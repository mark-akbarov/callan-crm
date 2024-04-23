// var swiper = new Swiper(".blog-slider", {
//   spaceBetween: 30,
//   effect: "fade",
//   loop: true,
//   mousewheel: {
//     invert: false,
//   },
//   // autoHeight: true,
//   pagination: {
//     el: ".blog-slider__pagination",
//     clickable: true,
//   },
// });

// !go link func
$(document).ready(function () {
  // Check if the URL contains a hash
  if (window.location.hash) {
    // Get the position of the section
    var sectionPos = $(window.location.hash).offset().top;

    // Subtract the height of the navbar and an additional 10 pixels from the position
    var navbarHeight = $(".navigation").outerHeight();
    sectionPos = sectionPos - navbarHeight - 30;

    // Scroll to the corresponding section
    $("html, body").animate(
      {
        scrollTop: sectionPos,
      },
      500
    );

    // Add a CSS class to highlight the section
    $(window.location.hash).addClass("highlighted");

    // Remove the highlight after some time
    setTimeout(function () {
      $(window.location.hash).removeClass("highlighted");
    }, 3000); // 3000 milliseconds = 3 seconds
  }
});
