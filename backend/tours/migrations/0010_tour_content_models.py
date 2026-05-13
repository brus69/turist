# Generated manually

from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    TourProgramDay = apps.get_model("tours", "TourProgramDay")
    TourIncludedItem = apps.get_model("tours", "TourIncludedItem")
    TourExcludedItem = apps.get_model("tours", "TourExcludedItem")
    TourPackingItem = apps.get_model("tours", "TourPackingItem")
    TourFaqItem = apps.get_model("tours", "TourFaqItem")

    for tour in Tour.objects.all():
        program = tour.program_by_day or []
        if isinstance(program, list):
            for idx, d in enumerate(program):
                if not isinstance(d, dict):
                    continue
                try:
                    dn = int(d.get("day") or idx + 1)
                except (TypeError, ValueError):
                    dn = idx + 1
                TourProgramDay.objects.create(
                    tour_id=tour.pk,
                    day_number=max(1, min(dn, 32767)),
                    title=str(d.get("title") or "")[:300],
                    body=str(d.get("body") or ""),
                    order=idx,
                )

        for model, field in (
            (TourIncludedItem, "included"),
            (TourExcludedItem, "not_included"),
            (TourPackingItem, "packing_list"),
        ):
            raw = getattr(tour, field) or []
            if not isinstance(raw, list):
                continue
            for idx, text in enumerate(raw):
                if not isinstance(text, str) or not text.strip():
                    continue
                model.objects.create(tour_id=tour.pk, text=text[:500], order=idx)

        faq = tour.faq or []
        if isinstance(faq, list):
            for idx, item in enumerate(faq):
                if not isinstance(item, dict):
                    continue
                TourFaqItem.objects.create(
                    tour_id=tour.pk,
                    question=str(item.get("q") or "")[:400],
                    answer=str(item.get("a") or ""),
                    order=idx,
                )


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0009_instructor_tourinstructor"),
    ]

    operations = [
        migrations.CreateModel(
            name="TourProgramDay",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("day_number", models.PositiveSmallIntegerField(default=1, verbose_name="Номер дня")),
                ("title", models.CharField(max_length=300, verbose_name="Заголовок")),
                ("body", models.TextField(blank=True, verbose_name="Описание")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="program_days",
                        to="tours.tour",
                        verbose_name="Тур",
                    ),
                ),
            ],
            options={
                "verbose_name": "День программы",
                "verbose_name_plural": "Программа по дням",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="TourIncludedItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=500, verbose_name="Текст")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="included_items",
                        to="tours.tour",
                        verbose_name="Тур",
                    ),
                ),
            ],
            options={
                "verbose_name": "Включено в стоимость",
                "verbose_name_plural": "Включено в стоимость",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="TourExcludedItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=500, verbose_name="Текст")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="excluded_items",
                        to="tours.tour",
                        verbose_name="Тур",
                    ),
                ),
            ],
            options={
                "verbose_name": "Не включено",
                "verbose_name_plural": "Не включено",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="TourPackingItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=500, verbose_name="Текст")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="packing_items",
                        to="tours.tour",
                        verbose_name="Тур",
                    ),
                ),
            ],
            options={
                "verbose_name": "Список вещей",
                "verbose_name_plural": "Список вещей",
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="TourFaqItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question", models.CharField(max_length=400, verbose_name="Вопрос")),
                ("answer", models.TextField(blank=True, verbose_name="Ответ")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="faq_items",
                        to="tours.tour",
                        verbose_name="Тур",
                    ),
                ),
            ],
            options={
                "verbose_name": "Вопрос и ответ",
                "verbose_name_plural": "Вопросы и ответы",
                "ordering": ["order", "id"],
            },
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
        migrations.RemoveField(model_name="tour", name="program_by_day"),
        migrations.RemoveField(model_name="tour", name="included"),
        migrations.RemoveField(model_name="tour", name="not_included"),
        migrations.RemoveField(model_name="tour", name="packing_list"),
        migrations.RemoveField(model_name="tour", name="faq"),
    ]
