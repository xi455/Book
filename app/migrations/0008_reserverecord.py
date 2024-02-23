# Generated by Django 4.2.7 on 2024-01-06 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0007_alter_book_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReserveRecord",
            fields=[
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="建立時間"),
                ),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新時間")),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "reserve_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="預約時間"
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="預約是否有效")),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.book"
                    ),
                ),
                (
                    "borrower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "預約記錄資訊",
                "verbose_name_plural": "預約記錄資訊",
            },
        ),
    ]
