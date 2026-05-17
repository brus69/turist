/**
 * Карточка тура: клик по фото галереи открывает полноэкранный просмотр.
 */
(function () {
  "use strict";

  var dataEl = document.getElementById("tour-gallery-urls");
  var root = document.querySelector("[data-tour-gallery]");
  if (!dataEl || !root) return;

  var urls;
  try {
    urls = JSON.parse(dataEl.textContent);
  } catch (e) {
    return;
  }
  if (!urls || !urls.length) return;

  var overlay = null;
  var imgEl = null;
  var btnPrev = null;
  var btnNext = null;
  var btnClose = null;
  var current = 0;
  var prevActive = null;

  function build() {
    overlay = document.createElement("div");
    overlay.className = "tour-lightbox";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Просмотр фотографии");
    overlay.classList.add("tour-lightbox--inactive");
    overlay.setAttribute("aria-hidden", "true");

    imgEl = document.createElement("img");
    imgEl.className = "tour-lightbox__img";
    imgEl.alt = "";

    btnClose = document.createElement("button");
    btnClose.type = "button";
    btnClose.className = "tour-lightbox__close";
    btnClose.setAttribute("aria-label", "Закрыть");
    btnClose.innerHTML = "&times;";

    btnPrev = document.createElement("button");
    btnPrev.type = "button";
    btnPrev.className = "tour-lightbox__nav tour-lightbox__nav--prev";
    btnPrev.setAttribute("aria-label", "Предыдущее фото");
    btnPrev.textContent = "‹";

    btnNext = document.createElement("button");
    btnNext.type = "button";
    btnNext.className = "tour-lightbox__nav tour-lightbox__nav--next";
    btnNext.setAttribute("aria-label", "Следующее фото");
    btnNext.textContent = "›";

    /* Сначала кадр, затем кнопки — чтобы крестик и стрелки были выше по стеку отрисовки */
    overlay.appendChild(imgEl);
    overlay.appendChild(btnPrev);
    overlay.appendChild(btnNext);
    overlay.appendChild(btnClose);

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) close();
    });
    imgEl.addEventListener("click", function (e) {
      e.stopPropagation();
    });
    btnClose.addEventListener("click", function (e) {
      e.stopPropagation();
      close();
    });
    btnPrev.addEventListener("click", function (e) {
      e.stopPropagation();
      show((current - 1 + urls.length) % urls.length);
    });
    btnNext.addEventListener("click", function (e) {
      e.stopPropagation();
      show((current + 1) % urls.length);
    });

    document.body.appendChild(overlay);
  }

  function show(index) {
    current = Math.max(0, Math.min(urls.length - 1, index));
    imgEl.src = urls[current];
    var multi = urls.length > 1;
    btnPrev.hidden = !multi;
    btnNext.hidden = !multi;
  }

  function isLightboxClosed() {
    return !overlay || overlay.classList.contains("tour-lightbox--inactive");
  }

  function open(index) {
    if (!overlay) build();
    show(index);
    overlay.classList.remove("tour-lightbox--inactive");
    overlay.setAttribute("aria-hidden", "false");
    document.body.classList.add("tour-lightbox-open");
    prevActive = document.activeElement;
    btnClose.focus();
  }

  function close() {
    if (!overlay) return;
    overlay.classList.add("tour-lightbox--inactive");
    overlay.setAttribute("aria-hidden", "true");
    imgEl.removeAttribute("src");
    document.body.classList.remove("tour-lightbox-open");
    if (prevActive && typeof prevActive.focus === "function") prevActive.focus();
  }

  function onKeydown(e) {
    if (isLightboxClosed()) return;
    if (e.key === "Escape") {
      e.preventDefault();
      close();
    } else if (e.key === "ArrowLeft" && urls.length > 1) {
      e.preventDefault();
      show((current - 1 + urls.length) % urls.length);
    } else if (e.key === "ArrowRight" && urls.length > 1) {
      e.preventDefault();
      show((current + 1) % urls.length);
    }
  }

  root.addEventListener("click", function (e) {
    var hit = e.target.closest("[data-gallery-index]");
    if (!hit || !root.contains(hit)) return;
    var idx = parseInt(hit.getAttribute("data-gallery-index"), 10);
    if (Number.isNaN(idx)) return;
    e.preventDefault();
    open(idx);
  });

  document.addEventListener("keydown", onKeydown);
})();
