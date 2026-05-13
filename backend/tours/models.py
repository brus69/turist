from urllib.parse import quote

from django.db import models


def picsum_url(seed: str, width: int = 800, height: int = 520) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in seed)[:80] or "turist"
    w, h = max(16, min(width, 2000)), max(16, min(height, 2000))
    return f"https://picsum.photos/seed/{quote(safe, safe='')}/{w}/{h}"


class Tour(models.Model):
    """Плоская модель тура + JSON для вложенных структур (как на фронте)."""

    slug = models.SlugField("slug", max_length=120, unique=True, db_index=True)
    title = models.CharField(max_length=512)
    region = models.CharField(max_length=200)
    country = models.CharField(max_length=120, default="Россия")
    activity_type = models.CharField(max_length=200)
    activity_kind = models.CharField(max_length=32)  # hike | kayak | horse | mountain
    difficulty = models.CharField(max_length=20)
    difficulty_score = models.PositiveSmallIntegerField(default=1)
    difficulty_max = models.PositiveSmallIntegerField(default=5)
    distance_km = models.PositiveIntegerField(default=0)
    duration_days = models.PositiveIntegerField(default=1)
    backpack_weight_kg = models.PositiveIntegerField(default=0)
    max_people = models.PositiveIntegerField(default=20)
    price = models.PositiveIntegerField()
    old_price = models.PositiveIntegerField(null=True, blank=True)
    currency = models.CharField(max_length=8, default="RUB")
    date_summary = models.CharField(max_length=255)
    gallery_extra_count = models.PositiveIntegerField(default=0)
    status_label = models.CharField(max_length=80, blank=True)
    spots_left = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    tags = models.JSONField(default=list)
    tags_secondary = models.JSONField(default=list)
    images = models.JSONField(default=list)
    breadcrumbs = models.JSONField(default=list)
    date_slots = models.JSONField(default=list)
    badges = models.JSONField(null=True, blank=True)
    program_by_day = models.JSONField(default=list)
    included = models.JSONField(default=list)
    not_included = models.JSONField(default=list)
    packing_list = models.JSONField(default=list)
    faq = models.JSONField(default=list)
    instructors = models.JSONField(default=list)
    season = models.JSONField(null=True, blank=True, default=list)
    holiday = models.JSONField(null=True, blank=True, default=list)
    duration_category = models.JSONField(null=True, blank=True, default=list)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.title
