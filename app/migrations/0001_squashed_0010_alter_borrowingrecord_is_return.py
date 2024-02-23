# Generated by Django 4.2.7 on 2024-02-22 07:59

import app.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    replaces = [
        ("app", "0001_initial"),
        ("app", "0002_alter_book_genre"),
        ("app", "0003_alter_book_published_date_and_more"),
        ("app", "0004_borrowingrecord_is_return"),
        ("app", "0005_book_picture"),
        ("app", "0006_book_admission_date"),
        ("app", "0007_alter_book_price"),
        ("app", "0008_reserverecord"),
        ("app", "0009_alter_reserverecord_reserve_date"),
        ("app", "0010_alter_borrowingrecord_is_return"),
    ]

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrower",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="建立時間"),
                ),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新時間")),
                (
                    "phone_number",
                    models.CharField(max_length=15, null=True, verbose_name="電話號碼"),
                ),
                ("address", models.TextField(null=True, verbose_name="地址")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "讀者帳號資訊",
                "verbose_name_plural": "讀者帳號資訊",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="建立時間"),
                ),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新時間")),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255, verbose_name="書名")),
                ("author", models.CharField(max_length=255, verbose_name="作者")),
                ("isbn", models.CharField(max_length=13, verbose_name="國際標準書號")),
                (
                    "published_date",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="出版日期"
                    ),
                ),
                (
                    "genre",
                    models.CharField(
                        choices=[
                            ("文學", "文學"),
                            ("兒童", "兒童"),
                            ("哲學", "哲學"),
                            ("英語", "英語"),
                            ("金融", "金融"),
                            ("程式", "程式"),
                            ("其他", "其他"),
                        ],
                        default="文學",
                        max_length=2,
                        verbose_name="類型",
                    ),
                ),
                ("quantity_in_stock", models.IntegerField(verbose_name="庫存數量")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="進貨價格"
                    ),
                ),
                ("description", models.TextField(verbose_name="描述")),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        db_comment="存放圖片路徑",
                        null=True,
                        upload_to=app.models.book_picture_directory_path,
                        verbose_name="圖片",
                    ),
                ),
                (
                    "admission_date",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="入館日期"
                    ),
                ),
            ],
            options={
                "verbose_name": "書本資訊",
                "verbose_name_plural": "書本資訊",
            },
        ),
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
                    models.DateField(
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
        migrations.CreateModel(
            name="BorrowingRecord",
            fields=[
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="建立時間"),
                ),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新時間")),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "borrow_date",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="借閱日期"
                    ),
                ),
                ("return_date", models.DateField(verbose_name="預計歸還日期")),
                (
                    "actual_return_date",
                    models.DateField(blank=True, null=True, verbose_name="實際歸還日期"),
                ),
                (
                    "fine_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="罰款金額",
                    ),
                ),
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
                (
                    "is_return",
                    models.BooleanField(blank=True, default=False, verbose_name="是否歸還"),
                ),
            ],
            options={
                "verbose_name": "借書紀錄",
                "verbose_name_plural": "借書紀錄",
            },
        ),
    ]
