(function () {
  const form = document.getElementById("catalog-filters-form");
  if (!form) {
    return;
  }

  function syncDatePlaceholders() {
    form.querySelectorAll(".catalog-filters__date-cell input[type=date]").forEach(function (inp) {
      const cell = inp.closest(".catalog-filters__date-cell");
      if (cell) {
        cell.classList.toggle("has-value", !!inp.value);
      }
    });
  }

  syncDatePlaceholders();

  let submitTimer = null;

  function scheduleSubmit() {
    if (submitTimer) {
      clearTimeout(submitTimer);
    }
    submitTimer = setTimeout(function () {
      form.requestSubmit();
    }, 350);
  }

  form.querySelectorAll("input[type=checkbox], input[type=radio]").forEach(function (el) {
    el.addEventListener("change", scheduleSubmit);
  });

  form.querySelectorAll("input[type=date], input[type=number], input[type=search]").forEach(function (el) {
    el.addEventListener("change", function () {
      if (el.type === "date") {
        syncDatePlaceholders();
      }
      scheduleSubmit();
    });
    el.addEventListener("blur", function () {
      if (el.type === "search" || el.type === "number") {
        scheduleSubmit();
      }
    });
  });

  const regionToggle = form.querySelector("[data-region-toggle]");
  if (regionToggle) {
    const collapsed = form.querySelectorAll(".catalog-filters__item--collapsed");
    regionToggle.addEventListener("click", function () {
      const expanded = regionToggle.getAttribute("aria-expanded") === "true";
      collapsed.forEach(function (item) {
        item.classList.toggle("is-visible", !expanded);
      });
      regionToggle.setAttribute("aria-expanded", expanded ? "false" : "true");
      regionToggle.textContent = expanded
        ? "показать ещё " + collapsed.length
        : "свернуть";
    });
  }
})();
