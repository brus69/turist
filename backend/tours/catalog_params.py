"""Парсинг и валидация GET-параметров каталога туров."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlencode

from .content_home import DIFFICULTY_LABELS, HOLIDAYS

MULTI_FILTER_KEYS = frozenset({"duration", "season", "holiday", "difficulty"})

ACTIVITY_KINDS = frozenset({"hike", "kayak", "horse", "mountain"})
HOLIDAY_VALUES = frozenset(h["value"] for h in HOLIDAYS)
DIFFICULTY_VALUES = frozenset(DIFFICULTY_LABELS.keys())


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [x.strip() for x in value.split(",") if x.strip()]


def _filter_allowed(values: list[str], allowed: frozenset[str]) -> list[str]:
    if not allowed:
        return values
    return [v for v in values if v in allowed]


@dataclass
class CatalogParams:
    """Нормализованные параметры каталога (для filter_tours и шаблонов)."""

    q: str = ""
    region: str = ""
    tag: str = ""
    activity: str = ""
    price_min: str = ""
    price_max: str = ""
    date_from: str = ""
    date_to: str = ""
    sort: str = "date"
    dir: str = "asc"
    avail: str = ""
    duration: list[str] = field(default_factory=list)
    season: list[str] = field(default_factory=list)
    holiday: list[str] = field(default_factory=list)
    difficulty: list[str] = field(default_factory=list)

    def as_filter_dict(self) -> dict[str, str]:
        """Словарь для filter_tours (мульти-поля — через запятую)."""
        out: dict[str, str] = {
            "q": self.q,
            "region": self.region,
            "tag": self.tag,
            "activity": self.activity,
            "priceMin": self.price_min,
            "priceMax": self.price_max,
            "from": self.date_from,
            "to": self.date_to,
            "sort": self.sort,
            "dir": self.dir,
            "avail": self.avail,
        }
        if self.duration:
            out["duration"] = ",".join(self.duration)
        if self.season:
            out["season"] = ",".join(self.season)
        if self.holiday:
            out["holiday"] = ",".join(self.holiday)
        if self.difficulty:
            out["difficulty"] = ",".join(self.difficulty)
        return out

    def query_pairs(self) -> list[tuple[str, str]]:
        """Пары (key, value) для urlencode с повторяющимися multi-ключами."""
        pairs: list[tuple[str, str]] = []
        d = self.as_filter_dict()
        for key, value in d.items():
            if key in MULTI_FILTER_KEYS:
                continue
            if value:
                pairs.append((key, value))
        for code in self.duration:
            pairs.append(("duration", code))
        for code in self.season:
            pairs.append(("season", code))
        for code in self.holiday:
            pairs.append(("holiday", code))
        for code in self.difficulty:
            pairs.append(("difficulty", code))
        return pairs

    def urlencode(self) -> str:
        return urlencode(self.query_pairs())


def catalog_params_from_request(
    request,
    *,
    duration_codes: frozenset[str] | None = None,
    season_codes: frozenset[str] | None = None,
) -> CatalogParams:
    """Разбор request.GET с валидацией кодов справочников."""
    duration_allowed = duration_codes or frozenset()
    season_allowed = season_codes or frozenset()

    duration_raw: list[str] = []
    season_raw: list[str] = []
    holiday_raw: list[str] = []
    difficulty_raw: list[str] = []

    for key in request.GET:
        if key in MULTI_FILTER_KEYS:
            parts = request.GET.getlist(key)
            if key == "duration":
                duration_raw = parts
            elif key == "season":
                season_raw = parts
            elif key == "holiday":
                holiday_raw = parts
            elif key == "difficulty":
                difficulty_raw = parts

    activity = (request.GET.get("activity") or "").strip()
    if activity not in ACTIVITY_KINDS:
        activity = ""

    return CatalogParams(
        q=(request.GET.get("q") or "").strip(),
        region=(request.GET.get("region") or "").strip(),
        tag=(request.GET.get("tag") or "").strip(),
        activity=activity,
        price_min=(request.GET.get("priceMin") or request.GET.get("price_min") or "").strip(),
        price_max=(request.GET.get("priceMax") or request.GET.get("price_max") or "").strip(),
        date_from=(request.GET.get("from") or request.GET.get("when_from") or "").strip(),
        date_to=(request.GET.get("to") or request.GET.get("when_to") or "").strip(),
        sort=(request.GET.get("sort") or "date").strip() or "date",
        dir=(request.GET.get("dir") or "asc").strip() or "asc",
        avail=(request.GET.get("avail") or "").strip(),
        duration=_filter_allowed(duration_raw, duration_allowed),
        season=_filter_allowed(season_raw, season_allowed),
        holiday=_filter_allowed(holiday_raw, HOLIDAY_VALUES),
        difficulty=_filter_allowed(difficulty_raw, DIFFICULTY_VALUES),
    )


def catalog_params_from_dict(params: dict[str, str]) -> CatalogParams:
    """Для unit-тестов filter_tours из плоского словаря."""
    activity = (params.get("activity") or "").strip()
    if activity not in ACTIVITY_KINDS:
        activity = ""
    return CatalogParams(
        q=(params.get("q") or "").strip(),
        region=(params.get("region") or "").strip(),
        tag=(params.get("tag") or "").strip(),
        activity=activity,
        price_min=(params.get("priceMin") or params.get("price_min") or "").strip(),
        price_max=(params.get("priceMax") or params.get("price_max") or "").strip(),
        date_from=(params.get("from") or params.get("when_from") or "").strip(),
        date_to=(params.get("to") or params.get("when_to") or "").strip(),
        sort=(params.get("sort") or "date").strip() or "date",
        dir=(params.get("dir") or "asc").strip() or "asc",
        avail=(params.get("avail") or "").strip(),
        duration=_filter_allowed(_parse_csv(params.get("duration")), frozenset()),
        season=_filter_allowed(_parse_csv(params.get("season")), frozenset()),
        holiday=_filter_allowed(_parse_csv(params.get("holiday")), HOLIDAY_VALUES),
        difficulty=_filter_allowed(_parse_csv(params.get("difficulty")), DIFFICULTY_VALUES),
    )


def merge_query_pairs(
    base_pairs: list[tuple[str, str]],
    **updates: Any,
) -> str:
    """Обновить query string: None/'' удаляет ключ; multi-ключи заменяются целиком."""
    by_key: dict[str, list[str]] = {}
    order: list[str] = []
    for key, value in base_pairs:
        if key not in by_key:
            by_key[key] = []
            order.append(key)
        by_key[key].append(value)

    for key, value in updates.items():
        if key in by_key:
            del by_key[key]
            order.remove(key)
        if value is None or value == "":
            continue
        by_key[key] = []
        if key not in order:
            order.append(key)
        if key in MULTI_FILTER_KEYS:
            if isinstance(value, (list, tuple)):
                by_key[key] = [str(v) for v in value if v]
            else:
                by_key[key] = [str(value)]
        else:
            by_key[key] = [str(value)]

    pairs: list[tuple[str, str]] = []
    for key in order:
        for v in by_key[key]:
            pairs.append((key, v))
    return urlencode(pairs)
