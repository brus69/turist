from __future__ import annotations

from django.shortcuts import render

from ..content_home import ACTIVITIES, ARTICLES, HERO_BG, REGIONS, REVIEWS, TRIP_PHOTOS, WHY_US
from ..filters import filter_tours
from ..models import Tour


def home(request):
    upcoming = filter_tours(
        Tour.objects.select_related("season", "duration_category").prefetch_related("gallery_images"),
        {"sort": "date", "dir": "asc"},
    )[:10]
    return render(
        request,
        "home.html",
        {
            "upcoming_tours": upcoming,
            "hero_bg": HERO_BG,
            "regions": REGIONS,
            "activities": ACTIVITIES,
            "trip_photos": TRIP_PHOTOS,
            "why_us": WHY_US,
            "articles": ARTICLES,
            "reviews": REVIEWS,
        },
    )
