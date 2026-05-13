from django.urls import path

from .views import TourDetailView, TourListView

urlpatterns = [
    path("tours/", TourListView.as_view(), name="tour-list"),
    path("tours/<slug:slug>/", TourDetailView.as_view(), name="tour-detail"),
]
