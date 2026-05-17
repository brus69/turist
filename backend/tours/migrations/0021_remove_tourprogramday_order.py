from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0020_instructor_slug_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tourprogramday",
            options={
                "ordering": ["day_number", "id"],
                "verbose_name": "День программы",
                "verbose_name_plural": "Программа по дням",
            },
        ),
        migrations.RemoveField(
            model_name="tourprogramday",
            name="order",
        ),
    ]
