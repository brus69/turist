"""Хлебные крошки карточки тура: строятся из страны и региона (без хранения в БД)."""

from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from django.urls import reverse

if TYPE_CHECKING:
    from .models import Tour


def tour_breadcrumb_links(tour: Tour) -> list[dict[str, str]]:
    """Элементы со ссылками для навигации (название тура в шаблоне добавляется отдельно)."""
    links: list[dict[str, str]] = [{"label": "Главная", "href": reverse("home")}]
    base = reverse("tour-catalog")
    country = (tour.country or "").strip()
    region = (tour.region or "").strip()
    if country:
        links.append({"label": country, "href": f"{base}?region={quote(country)}"})
    if region and region != country:
        links.append({"label": region, "href": f"{base}?region={quote(region)}"})
    return links
