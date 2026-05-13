"""Виджеты для админки."""

from django import forms
from django.utils.html import escape
from django.utils.safestring import mark_safe


class DateSlotsCalendarWidget(forms.Textarea):
    """
    JSON слотов дат + календарь и таблица редактирования (синхронизация с textarea).
    Ожидается массив объектов: id, label, start, end (даты ISO YYYY-MM-DD).
    """

    class Media:
        css = {"all": ("tours/admin_date_slots.css",)}
        js = ("js/date_slot_calendar_shared.js", "tours/admin_date_slots.js")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"].setdefault("rows", 10)
        kwargs["attrs"].setdefault("cols", 80)
        cls = kwargs["attrs"].get("class", "")
        kwargs["attrs"]["class"] = (cls + " admin-date-slots-json-field admin-date-slots-json-hidden").strip()
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        textarea_html = super().render(name, value, attrs, renderer)
        eid = escape(attrs.get("id", f"id_{name}"))
        html = (
            f'<div class="admin-date-slots-wrap" data-textarea-id="{eid}">'
            '<p class="help">Редактируйте слоты в таблице. Календарь подсвечивает диапазоны слотов.</p>'
            '<div class="admin-date-slots-cal-header">'
            '<button type="button" class="button admin-date-slots-cal-prev">‹</button>'
            '<span class="admin-date-slots-cal-title"></span>'
            '<button type="button" class="button admin-date-slots-cal-next">›</button>'
            "</div>"
            f'<div class="admin-date-slots-cal-root" id="{eid}_cal"></div>'
            '<table class="admin-date-slots-table"><thead><tr>'
            "<th>id</th><th>Подпись</th><th>Начало</th><th>Конец</th><th></th>"
            "</tr></thead>"
            f'<tbody id="{eid}_tbody"></tbody></table>'
            f'<p><button type="button" class="button" id="{eid}_addslot">Добавить слот</button></p>'
            f"{textarea_html}"
            "</div>"
        )
        return mark_safe(html)
