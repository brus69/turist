"""Фильтрация и сортировка туров: ORM + денормализованный first_start и TourDateSlot для дат."""

from __future__ import annotations

from datetime import date
from functools import cmp_to_key, reduce
from operator import or_

from django.db.models import Exists, OuterRef, Q, QuerySet

from .catalog_params import ACTIVITY_KINDS, CatalogParams, catalog_params_from_dict
from .models import Tour, TourDateSlot
from .tour_text_search import search_terms, tour_text_search_q

DIFFICULTY_ORDER = {"easy": 1, "medium": 2, "hard": 3, "very_hard": 4}


def _first_start_sort_key(t: Tour) -> str:
    if t.first_start:
        return t.first_start.isoformat()
    return ""


def apply_catalog_filters(qs: QuerySet[Tour], params: CatalogParams | dict[str, str]) -> QuerySet[Tour]:
    if isinstance(params, dict):
        params = catalog_params_from_dict(params)

    if params.q:
        terms = search_terms(params.q)
        text_q = tour_text_search_q(terms)
        if text_q is not None:
            qs = qs.filter(text_q)

    if params.region:
        qs = qs.filter(Q(region__name=params.region) | Q(country=params.region))

    if params.tag:
        qs = qs.filter(tags__name=params.tag)

    if params.activity:
        qs = qs.filter(activity_kind=params.activity)

    try:
        pmin = int(params.price_min) if params.price_min else None
    except (ValueError, TypeError):
        pmin = None
    try:
        pmax = int(params.price_max) if params.price_max else None
    except (ValueError, TypeError):
        pmax = None
    if pmin is not None:
        qs = qs.filter(price__gte=pmin)
    if pmax is not None:
        qs = qs.filter(price__lte=pmax)

    if params.duration:
        qs = qs.filter(duration_category__code__in=params.duration)

    if params.season:
        qs = qs.filter(season__code__in=params.season)

    if params.holiday:
        # SQLite не поддерживает JSON contains; ищем код праздника в сериализованном массиве.
        qs = qs.filter(reduce(or_, [Q(holiday__icontains=f'"{h}"') for h in params.holiday]))

    if params.difficulty:
        qs = qs.filter(difficulty__in=params.difficulty)

    if params.date_from or params.date_to:
        f_str = params.date_from or "1970-01-01"
        to_str = params.date_to or "2999-12-31"
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

    return qs.distinct()


def sort_tours(items: list[Tour], params: CatalogParams | dict[str, str]) -> list[Tour]:
    if isinstance(params, dict):
        params = catalog_params_from_dict(params)

    sort = params.sort or "date"
    desc = params.dir == "desc"
    avail_first = params.avail == "1"

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


def filter_tours(qs: QuerySet[Tour], params: CatalogParams | dict[str, str]) -> list[Tour]:
    qs = apply_catalog_filters(qs.prefetch_related("tags"), params)
    return sort_tours(list(qs), params)
