from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.site_search, name="site-search"),
    path("instructors/", views.instructor_list, name="instructor-list"),
    path("instructors/<slug:slug>/", views.instructor_detail, name="instructor-detail"),
    path("tours/", views.tour_catalog, name="tour-catalog"),
    path("tours/<slug:slug>/", views.tour_detail, name="tour-detail"),
]
