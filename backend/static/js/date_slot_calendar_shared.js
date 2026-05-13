/**
 * Общие константы и утилиты календаря слотов (сайт + админка).
 * Зависимостей нет; после загрузки доступен window.TuristDateSlotCal.
 */
(function (global) {
  const MONTHS = [
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
  const WD = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"];

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  /** ISO YYYY-MM-DD: y — год, m0 — месяц 0..11, d — число месяца */
  function toISO(y, m0, d) {
    return `${y}-${pad2(m0 + 1)}-${pad2(d)}`;
  }

  function slotIndexForDay(slots, dayStr) {
    for (let i = 0; i < slots.length; i++) {
      const s = slots[i];
      if (s.start && s.end && dayStr >= s.start && dayStr <= s.end) return i;
    }
    return -1;
  }

  function slotForDay(slots, dayStr) {
    for (const s of slots) {
      const a = s.start;
      const b = s.end;
      if (a && b && dayStr >= a && dayStr <= b) return s;
    }
    return null;
  }

  function firstMonthFromSlots(slots) {
    const withStart = slots.filter((s) => s.start).sort((a, b) => a.start.localeCompare(b.start));
    if (!withStart.length) return new Date();
    const p = withStart[0].start.split("-").map(Number);
    return new Date(p[0], p[1] - 1, 1);
  }

  global.TuristDateSlotCal = {
    MONTHS,
    WD,
    pad2,
    toISO,
    slotIndexForDay,
    slotForDay,
    firstMonthFromSlots,
  };
})(typeof window !== "undefined" ? window : globalThis);
