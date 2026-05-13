# Generated manually: галерея вместо JSON images.

from django.db import migrations, models
import django.db.models.deletion


def forwards_copy_images_to_gallery(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    TourGalleryImage = apps.get_model("tours", "TourGalleryImage")
    for tour in Tour.objects.all():
        urls = tour.images
        if not isinstance(urls, list):
            continue
        for idx, u in enumerate(urls):
            if not isinstance(u, str) or not u.strip():
                continue
            TourGalleryImage.objects.create(tour_id=tour.pk, url=u[:512], order=idx)


def backwards_restore_images_json(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    TourGalleryImage = apps.get_model("tours", "TourGalleryImage")
    for tour in Tour.objects.all():
        rows = list(
            TourGalleryImage.objects.filter(tour_id=tour.pk)
            .order_by("order", "id")
            .values_list("url", flat=True)
        )
        tour.images = rows
        tour.save(update_fields=["images"])


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0011_remove_tour_breadcrumbs"),
    ]

    operations = [
        migrations.CreateModel(
            name="TourGalleryImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("url", models.URLField(max_length=512, verbose_name="URL изображения")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery_images",
                        to="tours.tour",
                        verbose_name="Тур",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение галереи",
                "verbose_name_plural": "Изображения галереи",
                "ordering": ["order", "id"],
            },
        ),
        migrations.RunPython(forwards_copy_images_to_gallery, backwards_restore_images_json),
        migrations.RemoveField(
            model_name="tour",
            name="images",
        ),
    ]
