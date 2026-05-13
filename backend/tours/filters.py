"""Фильтрация и сортировка туров (как на фронте)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet

from .models import Tour

DIFFICULTY_ORDER = {"easy": 1, "medium": 2, "hard": 3, "very_hard": 4}


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [x for x in value.split(",") if x]


def _first_start(t: Tour) -> str:
    slots = t.date_slots or []
    if not slots:
        return ""
    return str(slots[0].get("start") or "")


def filter_tours(qs: QuerySet[Tour], params: dict[str, str]) -> list[Tour]:
    items = list(qs)

    q = (params.get("q") or "").strip().lower()
    if q:
        items = [t for t in items if q in t.title.lower()]

    region = params.get("region")
    if region:
        items = [t for t in items if t.region == region or t.country == region]

    activity = params.get("activity")
    if activity:
        kinds = {"hike", "kayak", "horse", "mountain"}
        if activity in kinds:
            items = [t for t in items if t.activity_kind == activity]
        else:
            low = activity.lower()
            items = [
                t
                for t in items
                if low in t.activity_type.lower() or any(low in tag.lower() for tag in (t.tags or []))
            ]

    try:
        pmin_raw = params.get("price_min") or params.get("priceMin")
        pmin = int(pmin_raw) if pmin_raw else None
    except (ValueError, TypeError):
        pmin = None
    try:
        pmax_raw = params.get("price_max") or params.get("priceMax")
        pmax = int(pmax_raw) if pmax_raw else None
    except (ValueError, TypeError):
        pmax = None
    if pmin is not None:
        items = [t for t in items if t.price >= pmin]
    if pmax is not None:
        items = [t for t in items if t.price <= pmax]

    duration_sel = _parse_csv(params.get("duration"))
    if duration_sel:
        items = [
            t
            for t in items
            if t.duration_category and any(d in t.duration_category for d in duration_sel)
        ]

    season_sel = _parse_csv(params.get("season"))
    if season_sel:
        items = [t for t in items if t.season and any(s in t.season for s in season_sel)]

    holiday_sel = _parse_csv(params.get("holiday"))
    if holiday_sel:
        items = [t for t in items if t.holiday and any(h in t.holiday for h in holiday_sel)]

    when_from = params.get("from") or params.get("when_from")
    when_to = params.get("to") or params.get("when_to")
    if when_from or when_to:
        f = when_from or "1970-01-01"
        to = when_to or "2999-12-31"

        def overlaps(slots: list) -> bool:
            for s in slots or []:
                if str(s.get("start", "")) <= to and str(s.get("end", "")) >= f:
                    return True
            return False

        items = [t for t in items if overlaps(t.date_slots)]

    sort = params.get("sort") or "date"
    dir_mul = -1 if (params.get("dir") or "asc") == "desc" else 1
    avail_first = params.get("avail") == "1"

    def cmp(a: Tour, b: Tour) -> int:
        if avail_first:
            pa = 0 if a.spots_left is not None else 1
            pb = 0 if b.spots_left is not None else 1
            if pa != pb:
                return pa - pb
            sa, sb = a.spots_left or 999, b.spots_left or 999
            if sa != sb:
                return sa - sb
        if sort == "price":
            return (a.price - b.price) * dir_mul
        if sort == "difficulty":
            return (DIFFICULTY_ORDER.get(a.difficulty, 0) - DIFFICULTY_ORDER.get(b.difficulty, 0)) * dir_mul
        da, db = _first_start(a), _first_start(b)
        if da < db:
            return -1 * dir_mul
        if da > db:
            return 1 * dir_mul
        return 0

    from functools import cmp_to_key

    items.sort(key=cmp_to_key(cmp))
    return items
