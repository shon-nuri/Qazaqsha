const sections = document.querySelectorAll("section");
const navLi = document.querySelectorAll(".navbar-nav .nav-link");

window.onscroll = () => {
  var current = "";
  sections.forEach((section) => {
    const sectionTop = section.offsetTop;
    if (pageYOffset >= sectionTop -500) {
      current = section.getAttribute("id"); }
  });
  navLi.forEach((li) => {
    li.classList.remove("active");
    if (li.href.includes(current)) {
        li.classList.add('active');
    }
  });
  
};
