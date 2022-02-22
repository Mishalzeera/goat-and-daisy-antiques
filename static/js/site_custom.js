function bodyFade() {
  gsap.from("#body", { opacity: 0, duration: 0.3 });
}

function goatAnim() {
  gsap.from("#goat", {
    duration: 7,
    opacity: 0,
  });
}

goat = document.getElementById("goatload");
goat.addEventListener("load", goatAnim());
