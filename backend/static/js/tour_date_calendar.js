/**
 * Выбор даты выезда: список слотов (value — индекс слота в массиве).
 */
(function () {
  "use strict";

  var dataEl = document.getElementById("tour-slots-data");
  var selectEl = document.getElementById("tour-slot-select");
  if (!dataEl || !selectEl) return;

  var slots;
  try {
    slots = JSON.parse(dataEl.textContent);
  } catch (e) {
    selectEl.innerHTML = "";
    var optErr = document.createElement("option");
    optErr.value = "";
    optErr.textContent = "Не удалось загрузить даты";
    selectEl.appendChild(optErr);
    selectEl.disabled = true;
    return;
  }
  if (!Array.isArray(slots) || slots.length === 0) {
    selectEl.innerHTML = "";
    var optEmpty = document.createElement("option");
    optEmpty.value = "";
    optEmpty.textContent = "Нет доступных дат";
    selectEl.appendChild(optEmpty);
    selectEl.disabled = true;
    return;
  }

  selectEl.innerHTML = "";
  for (var i = 0; i < slots.length; i++) {
    var s = slots[i];
    if (!s || typeof s !== "object") continue;
    if (!s.start || !s.end) continue;
    var label = (s.label && String(s.label).trim()) || "Дата " + (i + 1);
    var opt = document.createElement("option");
    opt.value = String(i);
    opt.textContent = label;
    selectEl.appendChild(opt);
  }

  if (selectEl.options.length === 0) {
    var o = document.createElement("option");
    o.value = "";
    o.textContent = "Нет доступных дат";
    selectEl.appendChild(o);
    selectEl.disabled = true;
    return;
  }

  selectEl.selectedIndex = 0;
})();
