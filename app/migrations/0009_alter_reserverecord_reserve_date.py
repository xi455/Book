# Generated by Django 4.2.7 on 2024-01-12 13:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0008_reserverecord"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reserverecord",
            name="reserve_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="預約時間"
            ),
        ),
    ]
