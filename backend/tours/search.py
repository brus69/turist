"""Глобальный поиск по турам и инструкторам."""

from __future__ import annotations

from django.db.models import Q, QuerySet

from .models import Instructor, Tour
from .tour_text_search import search_terms, tour_text_search_q


def search_tours(qs: QuerySet[Tour], q: str) -> list[Tour]:
    q = (q or "").strip()
    if not q:
        return []
    terms = search_terms(q)
    text_q = tour_text_search_q(terms)
    if text_q is None:
        return []
    return list(qs.filter(text_q).distinct().order_by("title", "id"))


def search_instructors(qs: QuerySet[Instructor], q: str) -> list[Instructor]:
    q = (q or "").strip()
    if not q:
        return []
    terms = search_terms(q)
    if not terms:
        return []
    flt = Q()
    for term in terms:
        flt &= Q(name__icontains=term) | Q(description__icontains=term)
    return list(qs.filter(flt).distinct().order_by("name", "slug"))
