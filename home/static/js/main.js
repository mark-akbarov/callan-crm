//  loader
function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("page").style.display = "block";
}

//event listeren
window.addEventListener("load", showPage);
let popup = document.querySelector(".popup");
let close = document.querySelector(".popup .close");
let enroll = document.querySelector(".popup .enroll");

popup.style.display = "block";
popup.style.visibility = "hidden";
setTimeout(() => {
  popup.style.visibility = "visible";
  popup.style.opacity = "1";
}, 1000);

function closePopup() {
  popup.style.opacity = "0";
  popup.style.visibility = "hidden";
  setTimeout(() => {
    popup.style.display = "none";
  }, 1000);
}

close.addEventListener("click", closePopup);
enroll.addEventListener("click", closePopup);

const dropdowns = document.querySelectorAll(".dropdown");

dropdowns.forEach((dropdown) => {
  const select = document.querySelector(".select");
  const caret = document.querySelector(".caret");
  const menu = document.querySelector(".menu");
  const options = document.querySelectorAll(".menu li");
  const selected = document.querySelector(".selected");
  select.addEventListener("click", () => {
    caret.classList.toggle("caret-rotate");
    menu.classList.toggle("menu-open");
  });

  options.forEach((option) => {
    option.addEventListener("click", () => {
      selected.classList.remove("placeholder");
      selected.innerText = option.innerText;
      caret.classList.remove("caret-rotate");
      menu.classList.remove("menu-open");
      options.forEach((option) => option.classList.remove("active"));
      option.classList.add("active");
    });
  });
});
document.addEventListener("DOMContentLoaded", function () {
  var links = document.querySelectorAll(".links a");

  links.forEach(function (link) {
    link.addEventListener("click", function () {
      // Remove active class from all links
      links.forEach(function (otherLink) {
        otherLink.classList.remove("active");
      });

      // Add active class to the clicked link
      this.classList.add("active");
    });
  });
});
function resetForm() {
  // Get all form elements and reset their values
  var formElements = document
    .getElementById("enroll")
    .querySelectorAll("input, textarea, select");
  formElements.forEach(function (element) {
    // Check if it's a dropdown, reset the selected index to the placeholder
    if (element.tagName.toLowerCase() === "select") {
      element.selectedIndex = 0;
    } else {
      // For other elements, reset their values
      element.value = "";
    }
  });
}
const marquee = document.querySelector(".marquee-content");

// Reset the marquee when it reaches the end
marquee.addEventListener("animationiteration", () => {
  marquee.style.animation = "none";
  setTimeout(() => {
    marquee.style.animation = "marquee 20s linear infinite"; // Adjust the duration and timing function as needed
  }, 0);
});

// Get the button element by its ID
const redirectButton = document.getElementById("about");

// Add a click event listener to the button
redirectButton.addEventListener("click", function () {
  // URL of the HTML file you want to redirect to
  const aboutPageUrl = "about.html";

  // Open the URL in a new tab
  window.open(aboutPageUrl, "_blank");
});
