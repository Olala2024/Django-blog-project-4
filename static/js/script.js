document.addEventListener("DOMContentLoaded", function () {
  const closeButtons = document.querySelectorAll(".btn-close");
  closeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const alertBox = this.parentElement;
      alertBox.style.display = "none";
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const navbarToggler = document.querySelector(".navbar-toggler");
  const navbarNav = document.querySelector("#navbarNav");

  if (navbarToggler) {
    navbarToggler.addEventListener("click", function () {
      navbarNav.classList.toggle("show");
    });
  }
});
