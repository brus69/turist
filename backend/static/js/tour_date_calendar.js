/**
 * Календарь выбора даты выезда по слотам тура (start/end — ISO YYYY-MM-DD).
 * Общие утилиты: date_slot_calendar_shared.js → TuristDateSlotCal.
 */
(function () {
  const C = window.TuristDateSlotCal;
  if (!C) return;

  const root = document.getElementById("tour-calendar-root");
  const dataEl = document.getElementById("tour-slots-data");
  const hiddenId = document.getElementById("tour-slot-id");
  const selectionEl = document.getElementById("tour-cal-selection");
  if (!root || !dataEl || !hiddenId) return;

  let slots;
  try {
    slots = JSON.parse(dataEl.textContent);
  } catch (e) {
    root.innerHTML = "<p class=\"muted\">Не удалось загрузить даты.</p>";
    return;
  }
  if (!Array.isArray(slots) || slots.length === 0) {
    root.innerHTML = "<p class=\"muted\">Нет доступных дат.</p>";
    return;
  }

  const { MONTHS, WD, toISO, slotForDay: slotForDayInSlots, firstMonthFromSlots } = C;

  function slotForDay(dayStr) {
    return slotForDayInSlots(slots, dayStr);
  }

  let view = firstMonthFromSlots(slots);
  let selectedDay = null;
  let selectedSlot = null;

  const first = slots.find((s) => s.start);
  if (first && first.start) {
    selectedDay = first.start;
    selectedSlot = slotForDay(selectedDay);
    hiddenId.value = selectedSlot ? selectedSlot.id : "";
    if (selectionEl && selectedSlot) {
      selectionEl.textContent = "Выбрано: " + selectedSlot.label;
    }
  }

  function render() {
    const y = view.getFullYear();
    const m0 = view.getMonth();
    const firstD = new Date(y, m0, 1);
    const mondayPad = (firstD.getDay() + 6) % 7;
    const daysInMonth = new Date(y, m0 + 1, 0).getDate();

    const header = document.createElement("div");
    header.className = "tour-cal-header";
    header.innerHTML =
      '<button type="button" class="tour-cal-nav" data-d="-1" aria-label="Предыдущий месяц">‹</button>' +
      '<span class="tour-cal-title"></span>' +
      '<button type="button" class="tour-cal-nav" data-d="1" aria-label="Следующий месяц">›</button>';
    header.querySelector(".tour-cal-title").textContent = `${MONTHS[m0]} ${y}`;

    header.querySelectorAll(".tour-cal-nav").forEach((btn) => {
      btn.addEventListener("click", () => {
        const dir = Number(btn.getAttribute("data-d"));
        view = new Date(y, m0 + dir, 1);
        render();
      });
    });

    const wdRow = document.createElement("div");
    wdRow.className = "tour-cal-weekdays";
    wdRow.innerHTML = WD.map((w) => `<span>${w}</span>`).join("");

    const grid = document.createElement("div");
    grid.className = "tour-cal-grid";

    for (let i = 0; i < mondayPad; i++) {
      const pad = document.createElement("div");
      pad.className = "tour-cal-day tour-cal-day--pad";
      grid.appendChild(pad);
    }

    for (let d = 1; d <= daysInMonth; d++) {
      const dayStr = toISO(y, m0, d);
      const slot = slotForDay(dayStr);
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "tour-cal-day";
      btn.textContent = String(d);
      btn.setAttribute("data-day", dayStr);

      if (slot) {
        btn.classList.add("tour-cal-day--available");
        if (
          selectedSlot &&
          dayStr >= selectedSlot.start &&
          dayStr <= selectedSlot.end
        ) {
          btn.classList.add("tour-cal-day--in-range");
        }
        if (selectedDay && dayStr === selectedDay) btn.classList.add("tour-cal-day--selected");
        btn.addEventListener("click", () => {
          selectedDay = dayStr;
          selectedSlot = slotForDay(dayStr);
          hiddenId.value = selectedSlot ? selectedSlot.id : "";
          if (selectionEl && selectedSlot) {
            selectionEl.textContent = "Выбрано: " + selectedSlot.label;
          }
          render();
        });
      }

      grid.appendChild(btn);
    }

    root.replaceChildren(header, wdRow, grid);
  }

  render();
})();
