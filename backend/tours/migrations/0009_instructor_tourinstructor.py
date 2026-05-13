# Generated manually

import re

from django.db import migrations, models
import django.db.models.deletion


def _norm_key(raw: str, tour_pk: int, idx: int) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(raw).strip())[:64].strip("-")
    return s or f"tour-{tour_pk}-instr-{idx}"


def forwards(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Instructor = apps.get_model("tours", "Instructor")
    TourInstructor = apps.get_model("tours", "TourInstructor")
    for tour in Tour.objects.all():
        data = tour.instructors or []
        if not isinstance(data, list):
            continue
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                continue
            kid = str(item.get("id") or "").strip()
            key = _norm_key(kid, tour.pk, idx)
            name = str(item.get("name") or key)[:200]
            av = str(item.get("avatarUrl") or "")[:512]
            inst, _ = Instructor.objects.get_or_create(key=key, defaults={"name": name, "avatar_url": av})
            TourInstructor.objects.get_or_create(tour=tour, instructor=inst, defaults={"order": idx})


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0008_durationcategory"),
    ]

    operations = [
        migrations.CreateModel(
            name="Instructor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "key",
                    models.SlugField(
                        help_text="Стабильный id, например из сидов",
                        max_length=64,
                        unique=True,
                        verbose_name="Ключ",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="Имя")),
                ("avatar_url", models.URLField(blank=True, max_length=512, verbose_name="Фото URL")),
            ],
            options={
                "verbose_name": "Инструктор",
                "verbose_name_plural": "Инструкторы",
                "ordering": ["name", "key"],
            },
        ),
        migrations.CreateModel(
            name="TourInstructor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "instructor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tour_links",
                        to="tours.instructor",
                        verbose_name="Инструктор",
                    ),
                ),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="instructor_links",
                        to="tours.tour",
                        verbose_name="Тур",
                    ),
                ),
            ],
            options={
                "verbose_name": "Инструктор в туре",
                "verbose_name_plural": "Инструкторы тура",
                "ordering": ["order", "id"],
            },
        ),
        migrations.AddConstraint(
            model_name="tourinstructor",
            constraint=models.UniqueConstraint(
                fields=("tour", "instructor"),
                name="tours_tourinstructor_unique_tour_instructor",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="tour",
            name="instructors",
        ),
    ]
