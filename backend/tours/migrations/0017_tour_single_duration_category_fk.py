# Generated manually: одна категория длительности на тур (FK вместо M2M).

import django.db.models.deletion
from django.db import migrations, models


def forwards_copy_first_duration(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    for tour in Tour.objects.all():
        first = tour.duration_categories.order_by("order", "code").first()
        did = first.pk if first else None
        Tour.objects.filter(pk=tour.pk).update(duration_category_id=did)


def backwards_restore_duration_m2m(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    for tour in Tour.objects.all():
        if tour.duration_category_id:
            tour.duration_categories.add(tour.duration_category_id)


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0016_tour_single_season_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="tour",
            name="duration_category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tours",
                to="tours.durationcategory",
                verbose_name="Категория длительности",
            ),
        ),
        migrations.RunPython(forwards_copy_first_duration, backwards_restore_duration_m2m),
        migrations.RemoveField(
            model_name="tour",
            name="duration_categories",
        ),
    ]
