const next = document.querySelector("#next");
const prev = document.querySelector("#prev");

function handleScrollNext() {
  const cards = document.querySelector(".card-content");
  const cardWidth = cards.offsetWidth;
  const scrollAmount =
    window.innerWidth / 2 > 600
      ? window.innerWidth / 2
      : window.innerWidth - 100;
  cards.scrollLeft += cardWidth + scrollAmount;
}

function handleScrollPrev() {
  const cards = document.querySelector(".card-content");
  const cardWidth = cards.offsetWidth;
  const scrollAmount =
    window.innerWidth / 2 > 600
      ? window.innerWidth / 2
      : window.innerWidth - 100;
  cards.scrollLeft -= cardWidth + scrollAmount;
}

next.addEventListener("click", handleScrollNext);
prev.addEventListener("click", handleScrollPrev);
