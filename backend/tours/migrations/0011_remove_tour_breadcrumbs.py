from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0010_tour_content_models"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tour",
            name="breadcrumbs",
        ),
    ]
