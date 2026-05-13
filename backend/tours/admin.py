from django.contrib import admin

from .forms import TourAdminForm
from .models import (
    DurationCategory,
    Instructor,
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


@admin.register(DurationCategory)
class DurationCategoryAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "order")
    list_editable = ("order",)
    ordering = ("order", "code")
    search_fields = ("code", "name")


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "order")
    list_editable = ("order",)
    ordering = ("order", "code")
    search_fields = ("code", "name")


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("key", "name", "avatar_url")
    search_fields = ("key", "name")


class TourGalleryImageInline(admin.TabularInline):
    model = TourGalleryImage
    extra = 1
    ordering = ("order", "id")
    fields = ("order", "url")


class TourProgramDayInline(admin.TabularInline):
    model = TourProgramDay
    extra = 0
    ordering = ("order", "id")
    fields = ("order", "day_number", "title", "body")


class TourIncludedItemInline(admin.TabularInline):
    model = TourIncludedItem
    extra = 1
    ordering = ("order", "id")
    fields = ("order", "text")


class TourExcludedItemInline(admin.TabularInline):
    model = TourExcludedItem
    extra = 1
    ordering = ("order", "id")
    fields = ("order", "text")


class TourPackingItemInline(admin.TabularInline):
    model = TourPackingItem
    extra = 1
    ordering = ("order", "id")
    fields = ("order", "text")


class TourFaqItemInline(admin.TabularInline):
    model = TourFaqItem
    extra = 0
    ordering = ("order", "id")
    fields = ("order", "question", "answer")


class TourInstructorInline(admin.TabularInline):
    model = TourInstructor
    extra = 1
    autocomplete_fields = ("instructor",)
    ordering = ("order", "id")
    fields = ("instructor", "order")


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    form = TourAdminForm
    inlines = (
        TourGalleryImageInline,
        TourProgramDayInline,
        TourIncludedItemInline,
        TourExcludedItemInline,
        TourPackingItemInline,
        TourFaqItemInline,
        TourInstructorInline,
    )
    list_display = ("id", "slug", "title", "region", "season", "duration_category", "price", "activity_kind", "difficulty")
    list_display_links = ("id", "slug", "title")
    search_fields = ("title", "slug", "region")
    list_filter = ("region", "activity_kind", "difficulty", "country")
    ordering = ("id",)

    fieldsets = (
        ("Основное", {"fields": ("slug", "title", "region", "country", "description")}),
        (
            "Активность и сложность",
            {
                "fields": (
                    "activity_type",
                    "activity_kind",
                    "difficulty",
                    "difficulty_score",
                    "difficulty_max",
                    "distance_km",
                    "duration_days",
                    "backpack_weight_kg",
                    "max_people",
                )
            },
        ),
        ("Цена и даты", {"fields": ("price", "old_price", "currency", "date_slots", "spots_left")}),
        ("Оформление карточки", {"fields": ("status_label", "tags")}),
        ("Фильтры каталога", {"fields": ("season", "duration_category")}),
    )


admin.site.site_header = "Администрирование сайта"
admin.site.site_title = "Админка"
admin.site.index_title = "Панель управления"
