# Generated by Django 4.2.7 on 2023-12-29 14:56

from django.db import migrations, models

import app.models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_borrowingrecord_is_return"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="picture",
            field=models.ImageField(
                blank=True,
                db_comment="存放圖片路徑",
                null=True,
                upload_to=app.models.book_picture_directory_path,
                verbose_name="圖片",
            ),
        ),
    ]
