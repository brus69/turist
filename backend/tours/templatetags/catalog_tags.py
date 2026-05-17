from django import template

from ..catalog_params import MULTI_FILTER_KEYS, catalog_params_from_request, merge_query_pairs

register = template.Library()


@register.simple_tag(takes_context=True)
def query_update(context, **kwargs):
    """Скопировать текущий GET и переопределить/удалить ключи (None или '' удаляют).

    Multi-параметры (duration, season, holiday, difficulty) сохраняют все значения.
    """
    request = context["request"]
    try:
        from ..models import DurationCategory, Season

        duration_codes = frozenset(DurationCategory.objects.values_list("code", flat=True))
        season_codes = frozenset(Season.objects.values_list("code", flat=True))
    except Exception:
        duration_codes = frozenset()
        season_codes = frozenset()

    params = catalog_params_from_request(
        request,
        duration_codes=duration_codes,
        season_codes=season_codes,
    )
    return merge_query_pairs(params.query_pairs(), **kwargs)
