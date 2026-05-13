# Generated manually for architecture plan

from datetime import date

from django.db import migrations, models
import django.db.models.deletion


def _first_start_from_slots(slots):
    if not slots:
        return None
    valid = [s for s in slots if s.get("start") and s.get("end")]
    if not valid:
        return None
    valid.sort(key=lambda s: str(s["start"]))
    try:
        return date.fromisoformat(str(valid[0]["start"])[:10])
    except ValueError:
        return None


def forwards_fill_slots(apps, schema_editor):
    Tour = apps.get_model("tours", "Tour")
    TourDateSlot = apps.get_model("tours", "TourDateSlot")
    for t in Tour.objects.iterator():
        slots = t.date_slots or []
        fs = _first_start_from_slots(slots)
        Tour.objects.filter(pk=t.pk).update(first_start=fs)
        TourDateSlot.objects.filter(tour_id=t.pk).delete()
        rows = []
        for pos, s in enumerate(slots):
            sd = ed = None
            if s.get("start"):
                try:
                    sd = date.fromisoformat(str(s["start"])[:10])
                except ValueError:
                    pass
            if s.get("end"):
                try:
                    ed = date.fromisoformat(str(s["end"])[:10])
                except ValueError:
                    pass
            rows.append(
                TourDateSlot(
                    tour_id=t.pk,
                    position=pos,
                    slot_key=str(s.get("id") or "")[:64],
                    label=str(s.get("label") or "")[:200],
                    start=sd,
                    end=ed,
                )
            )
        if rows:
            TourDateSlot.objects.bulk_create(rows)


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0005_date_slots_help_summary"),
    ]

    operations = [
        migrations.CreateModel(
            name="TourDateSlot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("position", models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")),
                ("slot_key", models.CharField(blank=True, max_length=64, verbose_name="id слота")),
                ("label", models.CharField(blank=True, max_length=200, verbose_name="Подпись")),
                ("start", models.DateField(blank=True, null=True, verbose_name="Начало")),
                ("end", models.DateField(blank=True, null=True, verbose_name="Конец")),
                (
                    "tour",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="date_slot_rows",
                        to="tours.tour",
                        verbose_name="Тур",
                    ),
                ),
            ],
            options={
                "verbose_name": "Слот даты",
                "verbose_name_plural": "Слоты дат",
                "ordering": ["position", "id"],
            },
        ),
        migrations.AddField(
            model_name="tour",
            name="first_start",
            field=models.DateField(
                blank=True,
                db_index=True,
                help_text="Заполняется из date_slots при сохранении (сортировка каталога в БД).",
                null=True,
                verbose_name="Первая дата выезда",
            ),
        ),
        migrations.RunPython(forwards_fill_slots, migrations.RunPython.noop),
    ]
