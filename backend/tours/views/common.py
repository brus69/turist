from __future__ import annotations

from ..catalog_params import MULTI_FILTER_KEYS, catalog_params_from_request

__all__ = ["MULTI_FILTER_KEYS", "catalog_params_from_request", "filter_params_from_request"]


def filter_params_from_request(request) -> dict[str, str]:
    """Параметры для filter_tours (совместимость с шаблонами get_params)."""
    duration_codes = frozenset()
    season_codes = frozenset()
    try:
        from ..models import DurationCategory, Season

        duration_codes = frozenset(DurationCategory.objects.values_list("code", flat=True))
        season_codes = frozenset(Season.objects.values_list("code", flat=True))
    except Exception:
        pass
    return catalog_params_from_request(
        request,
        duration_codes=duration_codes,
        season_codes=season_codes,
    ).as_filter_dict()
