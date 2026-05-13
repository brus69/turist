# Generated manually

from django.db import migrations, models


def forwards(apps, schema_editor):
    Season = apps.get_model("tours", "Season")
    Tour = apps.get_model("tours", "Tour")
    for code, name, order in [
        ("summer", "Лето", 1),
        ("winter", "Зима", 2),
        ("spring", "Весна", 3),
        ("autumn", "Осень", 4),
    ]:
        Season.objects.get_or_create(code=code, defaults={"name": name, "order": order})

    for tour in Tour.objects.all():
        raw = tour.season or []
        if not isinstance(raw, list):
            raw = []
        pks = list(
            Season.objects.filter(code__in=[c for c in raw if isinstance(c, str)]).values_list("id", flat=True)
        )
        tour.seasons.set(pks)


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0006_tour_first_start_tourdateslot"),
    ]

    operations = [
        migrations.CreateModel(
            name="Season",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=32, unique=True, verbose_name="Код")),
                ("name", models.CharField(max_length=64, verbose_name="Название")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок в списках")),
            ],
            options={
                "verbose_name": "Сезон",
                "verbose_name_plural": "Сезоны",
                "ordering": ["order", "code"],
            },
        ),
        migrations.AddField(
            model_name="tour",
            name="seasons",
            field=models.ManyToManyField(
                blank=True,
                related_name="tours",
                to="tours.season",
                verbose_name="Сезоны",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="tour",
            name="season",
        ),
    ]
