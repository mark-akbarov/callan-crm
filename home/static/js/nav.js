(function ($) {
  $(function () {
    // Function to toggle the mobile menu
    $("#nav-toggle").click(function () {
      $("nav ul").slideToggle(100); // Adjust the duration for smoother animation
      $(this).toggleClass("active");
    });

    // Function to toggle the dropdown menus
    $("nav ul li > a:not(:only-child)").click(function (e) {
      var $dropdown = $(this).siblings(".nav-dropdown");
      $dropdown.slideToggle(100); // Adjust the duration for smoother animation
      $(".nav-dropdown").not($dropdown).hide();
      e.stopPropagation();
    });

    // Hide dropdown menus when clicking outside
    $("html").click(function () {
      $(".nav-dropdown").hide();
    });
  });
})(jQuery);
