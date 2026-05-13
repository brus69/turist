from django.contrib import admin

from .models import Tour


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "title", "region", "price", "activity_kind")
    search_fields = ("title", "slug", "region")
