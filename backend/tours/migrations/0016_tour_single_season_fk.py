# Generated manually: один сезон на тур (FK вместо M2M).

import django.db.models.deletion
from django.db import migrations, models


def forwards_copy_first_season(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    for tour in Tour.objects.all():
        first = tour.seasons.order_by("order", "code").first()
        sid = first.pk if first else None
        Tour.objects.filter(pk=tour.pk).update(season_id=sid)


def backwards_restore_m2m(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    for tour in Tour.objects.all():
        if tour.season_id:
            tour.seasons.add(tour.season_id)


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0015_remove_tour_badges"),
    ]

    operations = [
        migrations.AddField(
            model_name="tour",
            name="season",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tours",
                to="tours.season",
                verbose_name="Сезон",
            ),
        ),
        migrations.RunPython(forwards_copy_first_season, backwards_restore_m2m),
        migrations.RemoveField(
            model_name="tour",
            name="seasons",
        ),
    ]
