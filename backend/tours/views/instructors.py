from __future__ import annotations

from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from ..models import Instructor, Tour


def instructor_list(request):
    instructors = (
        Instructor.objects.annotate(tour_count=Count("tour_links", distinct=True))
        .order_by("name", "slug")
    )
    return render(
        request,
        "instructors/list.html",
        {"instructors": instructors},
    )


def instructor_detail(request, slug: str):
    instructor = get_object_or_404(Instructor.objects.all(), slug=slug)
    tours = (
        Tour.objects.filter(instructor_links__instructor=instructor)
        .select_related("region")
        .distinct()
        .order_by("title")[:16]
    )
    return render(
        request,
        "instructors/detail.html",
        {
            "instructor": instructor,
            "instructor_tours": tours,
        },
    )
