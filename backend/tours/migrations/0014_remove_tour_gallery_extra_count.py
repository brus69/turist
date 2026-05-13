# Generated manually

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0013_remove_tour_tags_secondary"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tour",
            name="gallery_extra_count",
        ),
    ]
