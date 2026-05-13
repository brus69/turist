"""Фильтрация и сортировка туров: ORM + денормализованный first_start и TourDateSlot для дат."""

from __future__ import annotations

from datetime import date
from functools import cmp_to_key, reduce
from operator import or_

from django.db.models import Exists, OuterRef, Q, QuerySet

from .models import Tour, TourDateSlot

DIFFICULTY_ORDER = {"easy": 1, "medium": 2, "hard": 3, "very_hard": 4}


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [x for x in value.split(",") if x]


def _first_start_sort_key(t: Tour) -> str:
    if t.first_start:
        return t.first_start.isoformat()
    return ""


def filter_tours(qs: QuerySet[Tour], params: dict[str, str]) -> list[Tour]:
    q = (params.get("q") or "").strip()
    if q:
        qs = qs.filter(title__icontains=q)

    region = params.get("region")
    if region:
        qs = qs.filter(Q(region=region) | Q(country=region))

    activity = params.get("activity")
    kinds = {"hike", "kayak", "horse", "mountain"}
    if activity and activity in kinds:
        qs = qs.filter(activity_kind=activity)

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
        qs = qs.filter(price__gte=pmin)
    if pmax is not None:
        qs = qs.filter(price__lte=pmax)

    duration_sel = _parse_csv(params.get("duration"))
    if duration_sel:
        qs = qs.filter(duration_category__code__in=duration_sel)

    season_sel = _parse_csv(params.get("season"))
    if season_sel:
        qs = qs.filter(season__code__in=season_sel)

    holiday_sel = _parse_csv(params.get("holiday"))
    if holiday_sel:
        qs = qs.filter(reduce(or_, [Q(holiday__contains=[h]) for h in holiday_sel]))

    when_from = params.get("from") or params.get("when_from")
    when_to = params.get("to") or params.get("when_to")
    if when_from or when_to:
        f_str = when_from or "1970-01-01"
        to_str = when_to or "2999-12-31"
        try:
            f_date = date.fromisoformat(f_str[:10])
        except ValueError:
            f_date = date.min
        try:
            to_date = date.fromisoformat(to_str[:10])
        except ValueError:
            to_date = date.max
        overlap = TourDateSlot.objects.filter(
            tour_id=OuterRef("pk"),
            start__isnull=False,
            end__isnull=False,
            start__lte=to_date,
            end__gte=f_date,
        )
        qs = qs.filter(Exists(overlap))

    sort = params.get("sort") or "date"
    desc = (params.get("dir") or "asc") == "desc"
    avail_first = params.get("avail") == "1"

    items = list(qs)

    if activity and activity not in kinds:
        low = activity.lower()
        items = [
            t
            for t in items
            if low in t.activity_type.lower() or any(low in tag.lower() for tag in (t.tags or []))
        ]

    def cmp(a: Tour, b: Tour) -> int:
        if avail_first:
            pa = 0 if a.spots_left is not None else 1
            pb = 0 if b.spots_left is not None else 1
            if pa != pb:
                return pa - pb
            sa, sb = a.spots_left or 999, b.spots_left or 999
            if sa != sb:
                return sa - sb
        dir_mul = -1 if desc else 1
        if sort == "price":
            if a.price != b.price:
                return (1 if a.price > b.price else -1) * dir_mul
        elif sort == "difficulty":
            da, db = DIFFICULTY_ORDER.get(a.difficulty, 0), DIFFICULTY_ORDER.get(b.difficulty, 0)
            if da != db:
                return (1 if da > db else -1) * dir_mul
        else:
            fa, fb = _first_start_sort_key(a), _first_start_sort_key(b)
            if fa < fb:
                return -1 * dir_mul
            if fa > fb:
                return 1 * dir_mul
        return 0

    items.sort(key=cmp_to_key(cmp))
    return items
