from __future__ import annotations

_MULTI_KEYS = frozenset({"duration", "season", "holiday"})


def filter_params_from_request(request) -> dict[str, str]:
    """Параметры для filter_tours: мульти-поля склеиваем через запятую."""
    out: dict[str, str] = {}
    for key in request.GET:
        if key in _MULTI_KEYS:
            parts = request.GET.getlist(key)
            if parts:
                out[key] = ",".join(parts)
        else:
            out[key] = request.GET.get(key, "")
    return out
