from __future__ import annotations

from django.shortcuts import render

from ..models import Instructor, Tour
from ..search import search_instructors, search_tours


def site_search(request):
    q = (request.GET.get("q") or "").strip()
    tours: list[Tour] = []
    instructors: list[Instructor] = []
    if q:
        tours = search_tours(
            Tour.objects.select_related("region").prefetch_related("gallery_images"),
            q,
        )
        instructors = search_instructors(Instructor.objects.all(), q)
    total = len(tours) + len(instructors)
    return render(
        request,
        "search.html",
        {
            "q": q,
            "tours": tours,
            "instructors": instructors,
            "total": total,
        },
    )
