from django.contrib import admin

from app.models import Book, Borrower, ReserveRecord, BorrowingRecord

# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "isbn",
        "genre",
        "quantity_in_stock",
        "price",
    )
    list_filter = ("title", "genre")


@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ("id", "username")


@admin.register(ReserveRecord)
class ReserveRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "borrower",
        "book",
        "reserve_date",
        "is_active",
    )
    list_filter = (
        "borrower",
        "book",
        "reserve_date",
        "is_active",
    )


@admin.register(BorrowingRecord)
class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "borrower",
        "borrow_date",
        "return_date",
        "actual_return_date",
        "fine_amount",
    )
    list_filter = (
        "book",
        "borrower",
        "borrow_date",
        "return_date",
        "actual_return_date",
    )
