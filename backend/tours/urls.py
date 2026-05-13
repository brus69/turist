from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tours/", views.tour_catalog, name="tour-catalog"),
    path("tours/<slug:slug>/", views.tour_detail, name="tour-detail"),
]
