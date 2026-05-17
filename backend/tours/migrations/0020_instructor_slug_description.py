# Instructor.slug + description; заполнение slug для существующих записей.

from django.db import migrations, models
from django.utils.text import slugify


def fill_instructor_slugs(apps, schema_editor):
    Instructor = apps.get_model("tours", "Instructor")
    for inst in Instructor.objects.all():
        if inst.slug:
            continue
        base = slugify(inst.name, allow_unicode=True) or inst.key or "instructor"
        s = base[:110]
        n = 1
        while Instructor.objects.filter(slug=s).exclude(pk=inst.pk).exists():
            suf = f"-{n}"
            s = (base[: max(1, 110 - len(suf))] + suf)[:120]
            n += 1
        inst.slug = s
        inst.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("tours", "0019_alter_tour_date_slots_help"),
    ]

    operations = [
        migrations.AddField(
            model_name="instructor",
            name="slug",
            field=models.SlugField(
                db_index=True,
                help_text="Адрес страницы: /instructors/ваш-слаг/",
                max_length=120,
                null=True,
                unique=True,
                verbose_name="Слаг (URL)",
            ),
        ),
        migrations.AddField(
            model_name="instructor",
            name="description",
            field=models.TextField(blank=True, help_text="Текст на персональной странице", verbose_name="Описание"),
        ),
        migrations.RunPython(fill_instructor_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="instructor",
            name="slug",
            field=models.SlugField(
                db_index=True,
                help_text="Адрес страницы: /instructors/ваш-слаг/",
                max_length=120,
                unique=True,
                verbose_name="Слаг (URL)",
            ),
        ),
    ]
