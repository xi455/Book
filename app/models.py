from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from utils.models import BaseModel

# Create your models here.


class Book(BaseModel):
    id = models.AutoField(primary_key=True)
    title = models.CharField("書名", max_length=255)
    author = models.CharField("作者", max_length=255)
    isbn = models.CharField("國際標準書號", max_length=13)
    published_date = models.DateField("出版日期", default=timezone.now)

    class state(models.TextChoices):
        FIRST_STATE = "文學", "文學"
        SECOND_STATE = "兒童", "兒童"
        THIRD_STATE = "哲學", "哲學"
        FOURTH_STATE = "英語", "英語"
        FIFTH_STATE = "金融", "金融"
        SIXTH_STATE = "程式", "程式"
        SEVEN_STATE = "其他", "其他"

    genre = models.CharField(
        verbose_name="類型",
        max_length=2,
        choices=state.choices,
        default=state.FIRST_STATE,
    )

    quantity_in_stock = models.IntegerField("庫存數量")
    price = models.DecimalField("價格", max_digits=10, decimal_places=2)
    # 這表示 price 可以儲存最多10位數的數字，其中包括小數點前後的位數，並且小數點後最多有2位。
    description = models.TextField("描述")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "書本資訊"
        verbose_name_plural = "書本資訊"


class Borrower(BaseModel, AbstractUser):
    phone_number = models.CharField("電話號碼", max_length=15, null=True)
    address = models.TextField("地址", null=True)

    REQUIRED_FIELDS: list = []

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "讀者帳號資訊"
        verbose_name_plural = "讀者帳號資訊"


class BorrowingRecord(BaseModel):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    borrower = models.ForeignKey(
        Borrower,
        on_delete=models.CASCADE,
    )
    borrow_date = models.DateField("借閱日期", default=timezone.now)
    return_date = models.DateField("預計歸還日期")
    actual_return_date = models.DateField("實際歸還日期", null=True, blank=True)
    fine_amount = models.DecimalField(
        "罰款金額", max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_return = models.BooleanField("是否歸還", default=False)

    class Meta:
        verbose_name = "借書紀錄"
        verbose_name_plural = "借書紀錄"
