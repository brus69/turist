/**
 * Админка: слоты дат — календарь + таблица ↔ JSON textarea.
 * Общие утилиты: static/js/date_slot_calendar_shared.js → TuristDateSlotCal.
 */
(function () {
  const C = window.TuristDateSlotCal;
  if (!C) return;
  const { MONTHS, WD, toISO, slotIndexForDay, firstMonthFromSlots } = C;

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

    function readRowsIntoSlots() {
      const out = [];
      tbody.querySelectorAll("tr").forEach((tr) => {
        const inputs = tr.querySelectorAll("input");
        if (inputs.length < 4) return;
        out.push({
          id: inputs[0].value.trim(),
          label: inputs[1].value.trim(),
          start: inputs[2].value,
          end: inputs[3].value,
        });
      });
      return out;
    }

    function renderTable(slots) {
      tbody.innerHTML = "";
      slots.forEach((slot) => {
        const tr = document.createElement("tr");

        const tdId = document.createElement("td");
        const inId = document.createElement("input");
        inId.type = "text";
        inId.className = "vTextField";
        inId.value = slot.id ?? "";
        tdId.appendChild(inId);

        const tdLabel = document.createElement("td");
        const inLabel = document.createElement("input");
        inLabel.type = "text";
        inLabel.className = "vTextField";
        inLabel.value = slot.label ?? "";
        tdLabel.appendChild(inLabel);

        const tdStart = document.createElement("td");
        const inStart = document.createElement("input");
        inStart.type = "date";
        inStart.value = slot.start ?? "";
        tdStart.appendChild(inStart);

        const tdEnd = document.createElement("td");
        const inEnd = document.createElement("input");
        inEnd.type = "date";
        inEnd.value = slot.end ?? "";
        tdEnd.appendChild(inEnd);

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

        tr.appendChild(tdId);
        tr.appendChild(tdLabel);
        tr.appendChild(tdStart);
        tr.appendChild(tdEnd);
        tr.appendChild(tdDel);

        tr.querySelectorAll("input").forEach((inp) => {
          inp.addEventListener("input", () => {
            writeSlots(readRowsIntoSlots());
            showError("");
            renderCalendar(readRowsIntoSlots());
          });
        });

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
      slots.push({ id: "", label: "", start: "", end: "" });
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
