from django.db import migrations, models


def migrate_tags_json_to_m2m(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    Tag = apps.get_model("tours", "Tag")
    for tour in Tour.objects.all():
        raw = tour.tags_legacy
        if not isinstance(raw, list):
            continue
        tags = []
        for name in raw:
            if isinstance(name, str) and name.strip():
                tag, _ = Tag.objects.get_or_create(name=name.strip()[:120])
                tags.append(tag)
        if tags:
            tour.tags.set(tags)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0021_remove_tourprogramday_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
                "ordering": ["name"],
            },
        ),
        migrations.RenameField(
            model_name="tour",
            old_name="tags",
            new_name="tags_legacy",
        ),
        migrations.AddField(
            model_name="tour",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                related_name="tours",
                to="tours.tag",
                verbose_name="Теги",
            ),
        ),
        migrations.RunPython(migrate_tags_json_to_m2m, noop),
        migrations.RemoveField(
            model_name="tour",
            name="tags_legacy",
        ),
    ]
