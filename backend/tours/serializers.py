from rest_framework import serializers

from .models import Tour


class TourSerializer(serializers.ModelSerializer):
    """camelCase ключей верхнего уровня — djangorestframework-camel-case."""

    id = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = [
            "id",
            "slug",
            "title",
            "region",
            "country",
            "activity_type",
            "activity_kind",
            "difficulty",
            "difficulty_score",
            "difficulty_max",
            "distance_km",
            "duration_days",
            "backpack_weight_kg",
            "max_people",
            "price",
            "old_price",
            "currency",
            "date_summary",
            "gallery_extra_count",
            "status_label",
            "spots_left",
            "description",
            "tags",
            "tags_secondary",
            "images",
            "breadcrumbs",
            "date_slots",
            "badges",
            "program_by_day",
            "included",
            "not_included",
            "packing_list",
            "faq",
            "instructors",
            "season",
            "holiday",
            "duration_category",
        ]

    def get_id(self, obj: Tour) -> str:
        return str(obj.pk)
