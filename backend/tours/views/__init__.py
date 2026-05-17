"""Публичные представления: главная, каталог, карточка тура, инструкторы."""

from .catalog import tour_catalog, tour_detail
from .common import filter_params_from_request
from .home import home
from .instructors import instructor_detail, instructor_list
from .search import site_search

__all__ = [
    "filter_params_from_request",
    "home",
    "instructor_detail",
    "instructor_list",
    "site_search",
    "tour_catalog",
    "tour_detail",
]
