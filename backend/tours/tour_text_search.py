"""Общий текстовый поиск по полям тура (каталог q= и страница /search/)."""

from __future__ import annotations

from django.db.models import Q


def search_terms(q: str) -> list[str]:
    return [t for t in (q or "").split() if t]


def tour_text_search_q(terms: list[str]) -> Q | None:
    """AND между словами; для каждого слова — OR по полям тура."""
    if not terms:
        return None
    flt = Q()
    for term in terms:
        flt &= (
            Q(title__icontains=term)
            | Q(description__icontains=term)
            | Q(activity_type__icontains=term)
            | Q(region__name__icontains=term)
            | Q(country__icontains=term)
            | Q(tags__name__icontains=term)
        )
    return flt
