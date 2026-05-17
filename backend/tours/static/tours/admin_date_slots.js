/**
 * Админка: слоты дат — календарь + таблица (только начало/конец) ↔ JSON textarea.
 * В textarea — JSON без id: только start/end; подпись в таблице — превью по датам (как на сайте после сохранения).
 * Общие утилиты: static/js/date_slot_calendar_shared.js → TuristDateSlotCal.
 */
(function () {
  const C = window.TuristDateSlotCal;
  if (!C) return;
  const { MONTHS, WD, toISO, slotIndexForDay, firstMonthFromSlots } = C;

  const MONTHS_GEN = [
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

  function parseIsoLocal(iso) {
    const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(iso || "").trim());
    if (!m) return null;
    const y = Number(m[1]);
    const mo = Number(m[2]) - 1;
    const d = Number(m[3]);
    if (mo < 0 || mo > 11 || d < 1 || d > 31) return null;
    const dt = new Date(y, mo, d);
    if (dt.getFullYear() !== y || dt.getMonth() !== mo || dt.getDate() !== d) return null;
    return dt;
  }

  function daysWordRu(n) {
    let x = Math.abs(n | 0) % 100;
    if (x >= 11 && x <= 14) return "дней";
    x = x % 10;
    if (x === 1) return "день";
    if (x >= 2 && x <= 4) return "дня";
    return "дней";
  }

  function formatSlotLabel(startIso, endIso) {
    const start = parseIsoLocal(startIso);
    const end = parseIsoLocal(endIso);
    if (!start || !end) return "—";
    const t0 = Date.UTC(start.getFullYear(), start.getMonth(), start.getDate());
    const t1 = Date.UTC(end.getFullYear(), end.getMonth(), end.getDate());
    const days = Math.round((t1 - t0) / 86400000) + 1;
    if (days < 1) return "—";
    const mg = MONTHS_GEN;
    const dw = daysWordRu(days);
    const sy = start.getFullYear();
    const sm = start.getMonth();
    const sd = start.getDate();
    const ey = end.getFullYear();
    const em = end.getMonth();
    const ed = end.getDate();
    if (t0 === t1) {
      return `${sd} ${mg[sm]} ${sy} - ${days} ${dw}`;
    }
    if (sy === ey && sm === em) {
      return `с ${sd} по ${ed} ${mg[sm]} ${sy} - ${days} ${dw}`;
    }
    if (sy === ey) {
      return `с ${sd} ${mg[sm]} по ${ed} ${mg[em]} ${sy} - ${days} ${dw}`;
    }
    return `с ${sd} ${mg[sm]} ${sy} по ${ed} ${mg[em]} ${ey} - ${days} ${dw}`;
  }

  function readRowsIntoSlots(tbody) {
    const out = [];
    tbody.querySelectorAll("tr").forEach((tr, i) => {
      const inputs = tr.querySelectorAll("input[type=date]");
      const start = inputs[0] ? inputs[0].value : "";
      const end = inputs[1] ? inputs[1].value : "";
      out.push({
        start,
        end,
      });
    });
    return out;
  }

  function initWrap(wrap) {
    const tid = wrap.getAttribute("data-textarea-id");
    const textarea = document.getElementById(tid);
    if (!textarea) return;

    const calRoot = document.getElementById(`${tid}_cal`);
    const tbody = document.getElementById(`${tid}_tbody`);
    const addBtn = document.getElementById(`${tid}_addslot`);
    const titleEl = wrap.querySelector(".admin-date-slots-cal-title");
    const btnPrev = wrap.querySelector(".admin-date-slots-cal-prev");
    const btnNext = wrap.querySelector(".admin-date-slots-cal-next");
    let view = new Date();
    let debounceTimer;

    const errEl = document.createElement("p");
    errEl.className = "admin-date-slots-error";
    errEl.style.display = "none";
    const header = wrap.querySelector(".admin-date-slots-cal-header");
    if (header) header.before(errEl);

    function readSlots() {
      try {
        const t = textarea.value.trim();
        if (!t) return [];
        const j = JSON.parse(t);
        return Array.isArray(j) ? j : [];
      } catch (e) {
        return null;
      }
    }

    function writeSlots(slots) {
      textarea.value = JSON.stringify(slots, null, 2);
    }

    function showError(msg) {
      if (msg) {
        errEl.textContent = msg;
        errEl.style.display = "block";
      } else {
        errEl.style.display = "none";
      }
    }

    function bindRow(tr) {
      tr.querySelectorAll("input[type=date]").forEach((inp) => {
        inp.addEventListener("input", () => {
          const span = tr.querySelector(".admin-date-slots-label-preview");
          if (span) {
            const inputs = tr.querySelectorAll("input[type=date]");
            span.textContent = formatSlotLabel(inputs[0] ? inputs[0].value : "", inputs[1] ? inputs[1].value : "");
          }
          writeSlots(readRowsIntoSlots(tbody));
          showError("");
          renderCalendar(readRowsIntoSlots(tbody));
        });
      });
    }

    function renderTable(slots) {
      tbody.innerHTML = "";
      slots.forEach((slot) => {
        const tr = document.createElement("tr");

        const tdStart = document.createElement("td");
        const inStart = document.createElement("input");
        inStart.type = "date";
        inStart.className = "vTextField";
        inStart.value = slot.start ?? "";
        tdStart.appendChild(inStart);

        const tdEnd = document.createElement("td");
        const inEnd = document.createElement("input");
        inEnd.type = "date";
        inEnd.className = "vTextField";
        inEnd.value = slot.end ?? "";
        tdEnd.appendChild(inEnd);

        const tdLabel = document.createElement("td");
        const span = document.createElement("span");
        span.className = "admin-date-slots-label-preview";
        span.textContent = formatSlotLabel(inStart.value, inEnd.value);
        tdLabel.appendChild(span);

        const tdDel = document.createElement("td");
        const del = document.createElement("button");
        del.type = "button";
        del.className = "button admin-date-slots-del";
        del.textContent = "Удалить";
        del.addEventListener("click", () => {
          const rows = [...tbody.querySelectorAll("tr")];
          const i = rows.indexOf(tr);
          const s = readSlots();
          if (s === null) return;
          s.splice(i, 1);
          writeSlots(s);
          syncAll();
        });
        tdDel.appendChild(del);

        tr.appendChild(tdStart);
        tr.appendChild(tdEnd);
        tr.appendChild(tdLabel);
        tr.appendChild(tdDel);

        bindRow(tr);
        tbody.appendChild(tr);
      });
    }

    function renderCalendar(slots) {
      if (!calRoot || !titleEl) return;
      const y = view.getFullYear();
      const m0 = view.getMonth();
      titleEl.textContent = `${MONTHS[m0]} ${y}`;

      const firstD = new Date(y, m0, 1);
      const mondayPad = (firstD.getDay() + 6) % 7;
      const daysInMonth = new Date(y, m0 + 1, 0).getDate();

      calRoot.innerHTML = "";
      WD.forEach((w) => {
        const c = document.createElement("div");
        c.className = "admin-date-slots-cal-wd";
        c.textContent = w;
        calRoot.appendChild(c);
      });
      for (let i = 0; i < mondayPad; i++) {
        const c = document.createElement("div");
        c.className = "admin-date-slots-cal-day admin-date-slots-cal-day--pad";
        calRoot.appendChild(c);
      }
      for (let d = 1; d <= daysInMonth; d++) {
        const dayStr = toISO(y, m0, d);
        const si = slotIndexForDay(slots, dayStr);
        const cell = document.createElement("div");
        cell.className = "admin-date-slots-cal-day";
        cell.textContent = String(d);
        if (si >= 0) {
          cell.classList.add(`admin-date-slots-cal-day--slot${si % 3}`);
        }
        calRoot.appendChild(cell);
      }
    }

    function syncAll() {
      const slots = readSlots();
      if (slots === null) {
        showError("Некорректный JSON в поле слотов.");
        return;
      }
      showError("");
      renderTable(slots);
      renderCalendar(slots);
    }

    btnPrev.addEventListener("click", () => {
      const y = view.getFullYear();
      const m0 = view.getMonth();
      view = new Date(y, m0 - 1, 1);
      const slots = readSlots();
      if (slots) renderCalendar(slots);
    });

    btnNext.addEventListener("click", () => {
      const y = view.getFullYear();
      const m0 = view.getMonth();
      view = new Date(y, m0 + 1, 1);
      const slots = readSlots();
      if (slots) renderCalendar(slots);
    });

    addBtn.addEventListener("click", () => {
      let slots = readSlots();
      if (slots === null) slots = [];
      slots.push({ start: "", end: "" });
      writeSlots(slots);
      syncAll();
    });

    textarea.addEventListener("input", () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        const slots = readSlots();
        if (slots === null) {
          showError("Некорректный JSON.");
          return;
        }
        showError("");
        view = firstMonthFromSlots(slots);
        renderTable(slots);
        renderCalendar(slots);
      }, 250);
    });

    const slots0 = readSlots();
    if (slots0 === null) {
      showError("Некорректный JSON в поле слотов.");
      view = new Date();
      renderCalendar([]);
      return;
    }
    view = firstMonthFromSlots(slots0);
    renderTable(slots0);
    renderCalendar(slots0);
  }

  function run() {
    document.querySelectorAll(".admin-date-slots-wrap").forEach(initWrap);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
