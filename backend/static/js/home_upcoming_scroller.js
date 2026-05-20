(function () {
  document.querySelectorAll("[data-horizontal-scroller]").forEach(function (wrap) {
    var track = wrap.querySelector(".scroller");
    var prev = wrap.querySelector(".scroller-nav--prev");
    var next = wrap.querySelector(".scroller-nav--next");
    if (!track || !prev || !next) {
      return;
    }

    var epsilon = 2;

    function scrollStep() {
      var item = track.firstElementChild;
      if (!item) {
        return Math.max(track.clientWidth * 0.85, 200);
      }
      var gap = parseFloat(getComputedStyle(track).gap) || 16;
      return item.offsetWidth + gap;
    }

    function maxScrollLeft() {
      return track.scrollWidth - track.clientWidth;
    }

    function canScroll() {
      return maxScrollLeft() > epsilon;
    }

    function atStart() {
      return track.scrollLeft <= epsilon;
    }

    function atEnd() {
      return track.scrollLeft >= maxScrollLeft() - epsilon;
    }

    function updateNav() {
      var enabled = canScroll();
      prev.disabled = !enabled;
      next.disabled = !enabled;
    }

    prev.addEventListener("click", function () {
      if (!canScroll()) {
        return;
      }
      if (atStart()) {
        track.scrollTo({ left: maxScrollLeft(), behavior: "auto" });
      } else {
        track.scrollBy({ left: -scrollStep(), behavior: "smooth" });
      }
    });

    next.addEventListener("click", function () {
      if (!canScroll()) {
        return;
      }
      if (atEnd()) {
        track.scrollTo({ left: 0, behavior: "auto" });
      } else {
        track.scrollBy({ left: scrollStep(), behavior: "smooth" });
      }
    });

    window.addEventListener("resize", updateNav);
    updateNav();
  });
})();
