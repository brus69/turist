/**
 * Календарь в hero-поиске: диапазон дат / диапазон месяцев, ±3 дня.
 */
(function () {
  "use strict";

  var MONTHS = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
  ];
  var MONTHS_GEN = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
  ];
  var WD = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"];

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function toISO(y, m0, d) {
    return y + "-" + pad2(m0 + 1) + "-" + pad2(d);
  }

  function parseISO(str) {
    if (!str || str.length < 10) return null;
    var p = str.slice(0, 10).split("-").map(Number);
    if (!p[0] || p[1] < 1 || p[1] > 12) return null;
    return new Date(p[0], p[1] - 1, p[2] || 1);
  }

  function addDays(date, n) {
    var d = new Date(date.getTime());
    d.setDate(d.getDate() + n);
    return d;
  }

  function lastDayOfMonth(y, m0) {
    return new Date(y, m0 + 1, 0).getDate();
  }

  function monthStart(d) {
    return new Date(d.getFullYear(), d.getMonth(), 1);
  }

  function sameDay(a, b) {
    return (
      a &&
      b &&
      a.getFullYear() === b.getFullYear() &&
      a.getMonth() === b.getMonth() &&
      a.getDate() === b.getDate()
    );
  }

  function sameMonth(a, b) {
    return a && b && a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth();
  }

  function normalizeRange(start, end) {
    if (!start) return { start: null, end: null };
    if (!end) return { start: start, end: start };
    if (end < start) return { start: end, end: start };
    return { start: start, end: end };
  }

  function formatDisplayRange(from, to) {
    if (!from) return "";
    var end = to || from;
    if (sameDay(from, end)) {
      return from.getDate() + " " + MONTHS_GEN[from.getMonth()] + " " + from.getFullYear();
    }
    if (from.getMonth() === end.getMonth() && from.getFullYear() === end.getFullYear()) {
      return (
        from.getDate() +
        "–" +
        end.getDate() +
        " " +
        MONTHS_GEN[from.getMonth()] +
        " " +
        from.getFullYear()
      );
    }
    return (
      from.getDate() +
      " " +
      MONTHS_GEN[from.getMonth()] +
      " " +
      from.getFullYear() +
      " – " +
      end.getDate() +
      " " +
      MONTHS_GEN[end.getMonth()] +
      " " +
      end.getFullYear()
    );
  }

  function formatDisplayPeriodRange(start, end) {
    if (!start) return "";
    var finish = end || start;
    if (sameMonth(start, finish)) {
      return MONTHS[start.getMonth()] + " " + start.getFullYear();
    }
    if (start.getFullYear() === finish.getFullYear()) {
      return MONTHS[start.getMonth()] + " – " + MONTHS[finish.getMonth()] + " " + start.getFullYear();
    }
    return (
      MONTHS[start.getMonth()] +
      " " +
      start.getFullYear() +
      " – " +
      MONTHS[finish.getMonth()] +
      " " +
      finish.getFullYear()
    );
  }

  function init() {
    var root = document.querySelector("[data-hero-date-picker]");
    if (!root) return;

    var displayInput = root.querySelector(".hero-date-picker__display");
    var hiddenFrom = root.querySelector('input[name="from"]');
    var hiddenTo = root.querySelector('input[name="to"]');
    if (!displayInput || !hiddenFrom || !hiddenTo) return;

    var today = new Date();
    today.setHours(0, 0, 0, 0);

    var state = {
      open: false,
      mode: "exact",
      flex: false,
      rangeStart: null,
      rangeEnd: null,
      periodStart: null,
      periodEnd: null,
      leftMonth: monthStart(today),
      rightMonth: monthStart(new Date(today.getFullYear(), today.getMonth() + 1, 1)),
    };

    var popup = document.createElement("div");
    popup.className = "hero-date-picker__popup";
    popup.hidden = true;
    popup.setAttribute("role", "dialog");
    popup.setAttribute("aria-modal", "true");
    popup.setAttribute("aria-label", "Выбор даты");
    document.body.appendChild(popup);
    popup.addEventListener("click", function (e) {
      e.stopPropagation();
    });
    displayInput.setAttribute("aria-expanded", "false");

    function getExactRange() {
      return normalizeRange(state.rangeStart, state.rangeEnd);
    }

    function getPeriodRange() {
      return normalizeRange(state.periodStart, state.periodEnd);
    }

    function syncHidden() {
      if (state.mode === "period") {
        var pr = getPeriodRange();
        if (!pr.start) {
          hiddenFrom.value = "";
          hiddenTo.value = "";
          displayInput.value = "";
          return;
        }
        var y0 = pr.start.getFullYear();
        var m0 = pr.start.getMonth();
        var y1 = pr.end.getFullYear();
        var m1 = pr.end.getMonth();
        hiddenFrom.value = toISO(y0, m0, 1);
        hiddenTo.value = toISO(y1, m1, lastDayOfMonth(y1, m1));
        displayInput.value = formatDisplayPeriodRange(pr.start, pr.end);
        return;
      }

      var r = getExactRange();
      if (!r.start) {
        hiddenFrom.value = "";
        hiddenTo.value = "";
        displayInput.value = "";
        return;
      }
      var from = r.start;
      var to = r.end;
      if (state.flex) {
        from = addDays(r.start, -3);
        to = addDays(r.end, 3);
      }
      hiddenFrom.value = toISO(from.getFullYear(), from.getMonth(), from.getDate());
      hiddenTo.value = toISO(to.getFullYear(), to.getMonth(), to.getDate());
      displayInput.value = formatDisplayRange(r.start, r.end);
    }

    function initFromQuery() {
      var from = parseISO(hiddenFrom.value);
      var to = parseISO(hiddenTo.value);
      if (!from) return;

      if (
        to &&
        from.getDate() === 1 &&
        to.getDate() === lastDayOfMonth(to.getFullYear(), to.getMonth())
      ) {
        var monthFrom = monthStart(from);
        var monthTo = monthStart(to);
        if (monthFrom <= monthTo) {
          state.mode = "period";
          state.periodStart = monthFrom;
          state.periodEnd = monthTo;
          state.leftMonth = monthStart(monthFrom);
          state.rightMonth = monthStart(
            new Date(Math.max(monthFrom.getFullYear(), monthTo.getFullYear()), Math.max(monthFrom.getMonth(), monthTo.getMonth()), 1)
          );
          if (state.rightMonth <= state.leftMonth) {
            state.rightMonth = shiftMonth(state.leftMonth, 1);
          }
          return;
        }
      }

      state.mode = "exact";
      if (!to || sameDay(from, to)) {
        state.rangeStart = from;
        state.rangeEnd = from;
      } else {
        var expanded = normalizeRange(addDays(from, 3), addDays(to, -3));
        if (
          state.flex ||
          (sameDay(from, addDays(expanded.start, -3)) && sameDay(to, addDays(expanded.end, 3)))
        ) {
          state.flex = true;
          state.rangeStart = expanded.start;
          state.rangeEnd = expanded.end;
        } else {
          state.rangeStart = from;
          state.rangeEnd = to;
        }
      }
      state.leftMonth = monthStart(state.rangeStart);
      state.rightMonth = monthStart(
        new Date(state.rangeStart.getFullYear(), state.rangeStart.getMonth() + 1, 1)
      );
    }

    function positionPopup() {
      var rect = root.getBoundingClientRect();
      var gap = 10;
      var width = Math.min(700, window.innerWidth - 32);
      var left = Math.max(16, Math.min(rect.left, window.innerWidth - width - 16));
      var top = rect.bottom + gap;
      if (top + 420 > window.innerHeight - 16) {
        top = Math.max(16, rect.top - 420 - gap);
      }
      popup.style.width = width + "px";
      popup.style.left = left + "px";
      popup.style.top = top + "px";
    }

    function setOpen(open) {
      state.open = open;
      popup.hidden = !open;
      root.classList.toggle("is-open", open);
      displayInput.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) {
        render();
        positionPopup();
      }
    }

    function toggleOpen(e) {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      setOpen(!state.open);
    }

    function shiftMonth(base, delta) {
      return new Date(base.getFullYear(), base.getMonth() + delta, 1);
    }

    function rangeHint() {
      if (state.mode === "period") {
        if (state.periodStart && !state.periodEnd) {
          return "Выберите конец периода (месяц)";
        }
        return "Выберите начало и конец периода";
      }
      if (state.rangeStart && !state.rangeEnd) {
        return "Выберите дату окончания";
      }
      return "Выберите дату начала и окончания";
    }

    function pickExactDay(d) {
      if (!state.rangeStart || (state.rangeStart && state.rangeEnd)) {
        state.rangeStart = d;
        state.rangeEnd = null;
        return;
      }
      var r = normalizeRange(state.rangeStart, d);
      state.rangeStart = r.start;
      state.rangeEnd = r.end;
    }

    function pickPeriodDay(d) {
      var m = monthStart(d);
      if (!state.periodStart || (state.periodStart && state.periodEnd)) {
        state.periodStart = m;
        state.periodEnd = null;
        return;
      }
      var r = normalizeRange(state.periodStart, m);
      state.periodStart = r.start;
      state.periodEnd = r.end;
    }

    function renderMonthPanel(panel, monthDate) {
      var y = monthDate.getFullYear();
      var m0 = monthDate.getMonth();
      var firstDow = (new Date(y, m0, 1).getDay() + 6) % 7;
      var daysInMonth = lastDayOfMonth(y, m0);
      var prevDays = lastDayOfMonth(y, m0 - 1);
      var exact = getExactRange();
      var period = getPeriodRange();

      var html = '<div class="hero-date-picker__cal" data-panel="' + panel + '">';
      html += '<div class="hero-date-picker__cal-head">';
      html +=
        '<button type="button" class="hero-date-picker__nav" data-nav="' +
        panel +
        '" data-dir="-1" aria-label="Предыдущий месяц">‹</button>';
      html += '<span class="hero-date-picker__month-title">' + MONTHS[m0] + " " + y + "</span>";
      html +=
        '<button type="button" class="hero-date-picker__nav" data-nav="' +
        panel +
        '" data-dir="1" aria-label="Следующий месяц">›</button>';
      html += "</div>";
      html += '<div class="hero-date-picker__wd">';
      for (var w = 0; w < 7; w++) {
        html += "<span>" + WD[w] + "</span>";
      }
      html += '</div><div class="hero-date-picker__days">';

      var cell = 0;
      for (var i = 0; i < firstDow; i++) {
        var d0 = prevDays - firstDow + i + 1;
        var pm = m0 === 0 ? 11 : m0 - 1;
        var py = m0 === 0 ? y - 1 : y;
        html += dayCell(py, pm, d0, true);
        cell++;
      }
      for (var day = 1; day <= daysInMonth; day++) {
        html += dayCell(y, m0, day, false);
        cell++;
      }
      var next = 1;
      while (cell % 7 !== 0) {
        var nm = m0 === 11 ? 0 : m0 + 1;
        var ny = m0 === 11 ? y + 1 : y;
        html += dayCell(ny, nm, next, true);
        next++;
        cell++;
      }
      html += "</div></div>";
      return html;

      function dayCell(cy, cm0, cd, outside) {
        var date = new Date(cy, cm0, cd);
        var cls = "hero-date-picker__day";
        if (outside) cls += " is-outside";

        if (state.mode === "exact") {
          var showFrom = exact.start;
          var showTo = exact.end;
          if (state.flex && exact.start) {
            showFrom = addDays(exact.start, -3);
            showTo = addDays(exact.end, 3);
          }
          if (showFrom && date >= showFrom && date <= showTo) {
            cls += " is-in-range";
          }
          if (exact.start && sameDay(date, exact.start)) cls += " is-range-start";
          if (exact.end && sameDay(date, exact.end)) cls += " is-range-end";
          if (exact.start && !exact.end && sameDay(date, exact.start)) {
            cls += " is-range-start is-range-end";
          }
        } else {
          var ps = period.start;
          var pe = period.end || period.start;
          if (ps) {
            var startDay = monthStart(ps);
            var endDay = new Date(pe.getFullYear(), pe.getMonth(), lastDayOfMonth(pe.getFullYear(), pe.getMonth()));
            if (date >= startDay && date <= endDay) cls += " is-in-period";
          }
        }

        return (
          '<button type="button" class="' +
          cls +
          '" data-day="' +
          toISO(cy, cm0, cd) +
          '">' +
          cd +
          "</button>"
        );
      }
    }

    function render() {
      var modeExact = state.mode === "exact";
      popup.innerHTML =
        '<p class="hero-date-picker__hint">' +
        rangeHint() +
        "</p>" +
        '<div class="hero-date-picker__modes">' +
        '<button type="button" class="hero-date-picker__mode' +
        (modeExact ? "" : " is-active") +
        '" data-mode="period">Месяц или период</button>' +
        '<button type="button" class="hero-date-picker__mode' +
        (modeExact ? " is-active" : "") +
        '" data-mode="exact">' +
        '<span class="hero-date-picker__mode-icon" aria-hidden="true"></span>Точные даты</button>' +
        "</div>" +
        '<div class="hero-date-picker__cals">' +
        renderMonthPanel("left", state.leftMonth) +
        renderMonthPanel("right", state.rightMonth) +
        "</div>" +
        '<div class="hero-date-picker__footer' +
        (modeExact ? "" : " is-hidden") +
        '">' +
        '<span class="hero-date-picker__flex-label">± 3 дня</span>' +
        '<label class="hero-date-picker__switch">' +
        '<input type="checkbox" class="hero-date-picker__flex-input"' +
        (state.flex ? " checked" : "") +
        ">" +
        '<span class="hero-date-picker__switch-ui"></span>' +
        "</label>" +
        "</div>";

      popup.querySelectorAll("[data-mode]").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          e.stopPropagation();
          state.mode = btn.getAttribute("data-mode");
          render();
          syncHidden();
        });
      });

      popup.querySelectorAll("[data-nav]").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          e.stopPropagation();
          var panel = btn.getAttribute("data-nav");
          var dir = Number(btn.getAttribute("data-dir"));
          if (panel === "left") {
            state.leftMonth = shiftMonth(state.leftMonth, dir);
            if (state.leftMonth >= state.rightMonth) {
              state.rightMonth = shiftMonth(state.leftMonth, 1);
            }
          } else {
            state.rightMonth = shiftMonth(state.rightMonth, dir);
            if (state.rightMonth <= state.leftMonth) {
              state.leftMonth = shiftMonth(state.rightMonth, -1);
            }
          }
          render();
        });
      });

      popup.querySelectorAll("[data-day]").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          e.stopPropagation();
          var d = parseISO(btn.getAttribute("data-day"));
          if (!d) return;
          if (state.mode === "period") {
            pickPeriodDay(d);
          } else {
            pickExactDay(d);
          }
          syncHidden();
          render();
        });
      });

      var flexInput = popup.querySelector(".hero-date-picker__flex-input");
      if (flexInput) {
        flexInput.addEventListener("change", function () {
          state.flex = flexInput.checked;
          syncHidden();
          render();
        });
      }
    }

    root.addEventListener("click", function (e) {
      if (popup.contains(e.target)) return;
      toggleOpen(e);
    });

    displayInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        toggleOpen(e);
      }
    });

    document.addEventListener("click", function (e) {
      if (!state.open) return;
      if (root.contains(e.target) || popup.contains(e.target)) return;
      setOpen(false);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && state.open) setOpen(false);
    });

    window.addEventListener("resize", function () {
      if (state.open) positionPopup();
    });

    window.addEventListener(
      "scroll",
      function () {
        if (state.open) positionPopup();
      },
      true
    );

    initFromQuery();
    syncHidden();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
