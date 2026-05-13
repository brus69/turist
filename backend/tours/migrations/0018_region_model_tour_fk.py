# Generated manually: Region + Tour.region FK, data from CharField `region`.

from django.db import migrations, models
import django.db.models.deletion


REGION_ORDER = [
    "Россия",
    "Карелия и Ленобласть",
    "Алтай",
    "Кавказ",
    "Байкал",
    "Архангельская область",
]


def _region_order(name: str) -> int:
    try:
        return REGION_ORDER.index(name)
    except ValueError:
        return len(REGION_ORDER) + abs(hash(name)) % 1000


def forwards(apps, schema_editor):
    Region = apps.get_model("tours", "Region")
    Tour = apps.get_model("tours", "Tour")
    for i, name in enumerate(REGION_ORDER):
        Region.objects.update_or_create(name=name, defaults={"order": i})
    for raw in Tour.objects.values_list("region", flat=True).distinct():
        s = (raw or "").strip()
        if not s:
            continue
        if not Region.objects.filter(name=s).exists():
            Region.objects.create(name=s, order=_region_order(s))
    default = Region.objects.filter(name="Россия").first()
    if default is None:
        default = Region.objects.order_by("order", "id").first()
    for t in Tour.objects.all():
        label = (getattr(t, "region", None) or "").strip()
        if not label:
            r = default
        else:
            r = Region.objects.filter(name=label).first()
            if r is None:
                r = Region.objects.create(name=label, order=_region_order(label))
        Tour.objects.filter(pk=t.pk).update(region_fk_id=r.pk)


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0017_tour_single_duration_category_fk"),
    ]

    operations = [
        migrations.CreateModel(
            name="Region",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, unique=True, verbose_name="Название")),
                ("order", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок в списках")),
            ],
            options={
                "verbose_name": "Регион",
                "verbose_name_plural": "Регионы",
                "ordering": ["order", "name"],
            },
        ),
        migrations.AddField(
            model_name="tour",
            name="region_fk",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tours",
                to="tours.region",
                verbose_name="Регион",
            ),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
        migrations.RemoveField(model_name="tour", name="region"),
        migrations.RenameField(model_name="tour", old_name="region_fk", new_name="region"),
        migrations.AlterField(
            model_name="tour",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="tours",
                to="tours.region",
                verbose_name="Регион",
            ),
        ),
    ]
