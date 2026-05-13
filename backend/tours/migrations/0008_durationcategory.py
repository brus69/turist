# Generated manually

from django.db import migrations, models


def forwards(apps, schema_editor):
    DurationCategory = apps.get_model("tours", "DurationCategory")
    Tour = apps.get_model("tours", "Tour")
    for code, name, order in [
        ("long", "Большие (от 5 дней)", 1),
        ("weekend", "На выходные", 2),
        ("oneday", "Однодневные", 3),
    ]:
        DurationCategory.objects.get_or_create(code=code, defaults={"name": name, "order": order})

    for tour in Tour.objects.all():
        raw = tour.duration_category or []
        if not isinstance(raw, list):
            raw = []
        pks = list(
            DurationCategory.objects.filter(code__in=[c for c in raw if isinstance(c, str)]).values_list(
                "id", flat=True
            )
        )
        tour.duration_categories.set(pks)


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0007_season_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="DurationCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(db_index=True, max_length=32, unique=True, verbose_name="Код")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок в списках")),
            ],
            options={
                "verbose_name": "Категория длительности",
                "verbose_name_plural": "Категории длительности",
                "ordering": ["order", "code"],
            },
        ),
        migrations.AddField(
            model_name="tour",
            name="duration_categories",
            field=models.ManyToManyField(
                blank=True,
                related_name="tours",
                to="tours.durationcategory",
                verbose_name="Категории длительности",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="tour",
            name="duration_category",
        ),
    ]
