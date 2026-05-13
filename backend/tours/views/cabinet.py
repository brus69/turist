from __future__ import annotations

from django.shortcuts import render

from ..content_home import CABINET_LINKS


def _cabinet(request, template: str, title: str):
    return render(
        request,
        template,
        {"cabinet_title": title, "cabinet_links": CABINET_LINKS},
    )


def cabinet_dashboard(request):
    return _cabinet(request, "cabinet/dashboard.html", "Обзор")


def cabinet_calendar(request):
    return _cabinet(request, "cabinet/calendar.html", "Календарь")


def cabinet_routes(request):
    return _cabinet(request, "cabinet/routes.html", "Маршруты")


def cabinet_media(request):
    return _cabinet(request, "cabinet/media.html", "Фото")


def cabinet_create_tour(request):
    return _cabinet(request, "cabinet/create_tour.html", "Создание тура")
