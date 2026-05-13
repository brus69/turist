# Generated manually

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tours", "0014_remove_tour_gallery_extra_count"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tour",
            name="badges",
        ),
    ]
