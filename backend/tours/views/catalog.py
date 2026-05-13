from __future__ import annotations

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from ..content_home import (
    ACTIVITIES,
    DIFFICULTY_LABELS,
    HOLIDAYS,
    REGIONS,
    reviews_for_tour,
)
from ..breadcrumbs import tour_breadcrumb_links
from ..filters import filter_tours
from ..models import (
    DurationCategory,
    Season,
    Tour,
    TourExcludedItem,
    TourFaqItem,
    TourGalleryImage,
    TourIncludedItem,
    TourInstructor,
    TourPackingItem,
    TourProgramDay,
)
from .common import filter_params_from_request


def tour_catalog(request):
    params = filter_params_from_request(request)
    tours = filter_tours(
        Tour.objects.select_related("season", "duration_category").prefetch_related("gallery_images"),
        params,
    )
    dur_sel = [x for x in (params.get("duration") or "").split(",") if x]
    season_sel = [x for x in (params.get("season") or "").split(",") if x]
    hol_sel = [x for x in (params.get("holiday") or "").split(",") if x]
    return render(
        request,
        "tours/catalog.html",
        {
            "tours": tours,
            "get_params": params,
            "duration_selected": dur_sel,
            "season_selected": season_sel,
            "holiday_selected": hol_sel,
            "regions": REGIONS,
            "activities": ACTIVITIES,
            "duration_filters": DurationCategory.objects.all(),
            "seasons": Season.objects.all(),
            "holidays": HOLIDAYS,
        },
    )


def tour_detail(request, slug: str):
    qs = Tour.objects.select_related("season", "duration_category").prefetch_related(
        Prefetch(
            "instructor_links",
            queryset=TourInstructor.objects.select_related("instructor").order_by("order", "id"),
        ),
        Prefetch("program_days", queryset=TourProgramDay.objects.order_by("order", "id")),
        Prefetch("included_items", queryset=TourIncludedItem.objects.order_by("order", "id")),
        Prefetch("excluded_items", queryset=TourExcludedItem.objects.order_by("order", "id")),
        Prefetch("packing_items", queryset=TourPackingItem.objects.order_by("order", "id")),
        Prefetch("faq_items", queryset=TourFaqItem.objects.order_by("order", "id")),
        Prefetch("gallery_images", queryset=TourGalleryImage.objects.order_by("order", "id")),
    )
    tour = get_object_or_404(qs, slug=slug)
    return render(
        request,
        "tours/detail.html",
        {
            "tour": tour,
            "breadcrumbs": tour_breadcrumb_links(tour),
            "tour_reviews": reviews_for_tour(tour.title),
            "difficulty_label": DIFFICULTY_LABELS.get(tour.difficulty, tour.difficulty),
        },
    )
