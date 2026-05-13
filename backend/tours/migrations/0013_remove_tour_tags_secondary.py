# Generated manually

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0012_tour_gallery_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tour",
            name="tags_secondary",
        ),
    ]
