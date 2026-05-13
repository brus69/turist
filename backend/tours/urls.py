from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tours/", views.tour_catalog, name="tour-catalog"),
    path("tours/<slug:slug>/", views.tour_detail, name="tour-detail"),
    path("cabinet/", views.cabinet_dashboard, name="cabinet-dashboard"),
    path("cabinet/calendar/", views.cabinet_calendar, name="cabinet-calendar"),
    path("cabinet/routes/", views.cabinet_routes, name="cabinet-routes"),
    path("cabinet/media/", views.cabinet_media, name="cabinet-media"),
    path("cabinet/create-tour/", views.cabinet_create_tour, name="cabinet-create-tour"),
]
