(function () {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".site-header__menu-toggle");
  const panel = document.getElementById("site-nav-panel");
  const backdrop = document.getElementById("site-nav-backdrop");
  if (!header || !toggle || !panel) {
    return;
  }

  const mq = window.matchMedia("(min-width: 992px)");

  function setOpen(open) {
    header.classList.toggle("is-nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");
    document.body.classList.toggle("is-nav-locked", open);
    if (backdrop) {
      backdrop.hidden = !open;
    }
  }

  toggle.addEventListener("click", function () {
    setOpen(!header.classList.contains("is-nav-open"));
  });

  if (backdrop) {
    backdrop.addEventListener("click", function () {
      setOpen(false);
    });
  }

  panel.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      setOpen(false);
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      setOpen(false);
    }
  });

  mq.addEventListener("change", function (event) {
    if (event.matches) {
      setOpen(false);
    }
  });

  if (document.body.classList.contains("page-home")) {
    var hero = document.querySelector(".page-home-hero");

    function updateHomeHeader() {
      var threshold = 48;
      if (hero) {
        threshold = Math.max(48, hero.offsetHeight - header.offsetHeight - 24);
      }
      header.classList.toggle("is-scrolled", window.scrollY > threshold);
    }

    updateHomeHeader();
    window.addEventListener("scroll", updateHomeHeader, { passive: true });
    window.addEventListener("resize", updateHomeHeader);
  }
})();
