# Generated by Django 4.2.7 on 2023-12-29 05:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_alter_book_published_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="borrowingrecord",
            name="is_return",
            field=models.BooleanField(default=False, verbose_name="是否歸還"),
        ),
    ]
