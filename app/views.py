from datetime import datetime, timedelta
from typing import Any

from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from app.forms import BookForm, BorrowerForm, BorrowerUpdateForm, ReserveRecordForm, BorrowingRecordForm, ReserveBorrowingRecordForm
from app.models import Book, Borrower, ReserveRecord, BorrowingRecord

# Create your views here.


class BookListItem(ListView):
    template_name = "book_list.html"
    model = Book
    context_object_name = "items"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("book_title")

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book_objects = Book.objects.all()
        overall_related_data = (
            book_objects.annotate(related_count=Count("borrowingrecord"))
            .values("id", "title", "related_count", "picture")
            .order_by("-related_count")[:5]
        )

        three_months_ago = datetime.now() - timedelta(days=90)
        newbook_related_data = (
            book_objects.filter(admission_date__gte=three_months_ago)
            .annotate(related_count=Count("borrowingrecord"))
            .values("id", "title", "related_count", "admission_date", "picture")
            .order_by("-related_count")
        )[:5]

        context["overall_related_data"] = overall_related_data
        context["newbook_related_data"] = newbook_related_data

        return context


class BorrowerListItem(ListView):
    template_name = "borrower_list.html"
    model = Borrower
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username")

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset


class RecordLendListItem(ListView):
    template_name = "book_lend_logs.html"
    model = BorrowingRecord
    context_object_name = "logs"
    paginate_by = 10
    ordering = "borrow_date"

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("book_title")

        if title:
            queryset = queryset.filter(
                Q(book__title__icontains=title) & Q(is_return=False)
            )
        else:
            queryset = queryset.filter(is_return=False)

        return queryset


class ReserveRecordListItem(ListView):
    template_name = "reserve_list.html"
    model = ReserveRecord
    context_object_name = "logs"
    paginate_by = 10
    ordering = "-is_active"

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username")

        if username:
            queryset = queryset.filter(
                Q(borrower__username__icontains=username)
            )

            return queryset

        # __lt 是一個過濾器，代表 "小於"（less than）。這個過濾器用於查詢某個字段的值小於特定值的對象。
        current_time = timezone.now()
        queryset_lt = queryset.filter(reserve_date__lt=current_time)

        queryset = queryset.filter(reserve_date__gt=current_time)

        for lt in queryset_lt:
            if lt.is_active:
                lt.is_active = False
                lt.book.quantity_in_stock += 1
                lt.book.save()
                print("ls.book.quantity_in_stock:", lt.book, lt.book.quantity_in_stock)

        # transaction.atomic() 的主要目的是確保資料庫操作的原子性，即一個事務中的所有操作都要麼全部成功，要麼全部失敗。
        # 如果事務中的任何操作失敗，則所有的更改都將被回滾，資料庫將保持原狀。
                
        # 使用 bulk_update 一次性保存修改
        with transaction.atomic():
            ReserveRecord.objects.bulk_update(queryset_lt, ["is_active"])

        return queryset
    

class ReservePersonListItem(ListView):
    template_name = "reserve_person_list.html"
    model = ReserveRecord
    context_object_name = "logs"
    paginate_by = 10
    ordering = "reserve_date"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(borrower__username=self.request.user)
        title = self.request.GET.get("book_title")

        if title:
            queryset = queryset.filter(
                Q(book__title__icontains=title)
            )

        return queryset


class RecordTimeOutListView(ListView):
    template_name = "record_list_time_out.html"
    model = BorrowingRecord
    context_object_name = "logs"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("book_title")

        # __icontains 代表著模糊查詢，不區分大小寫區別
        if title:
            queryset = queryset.filter(
                Q(book__title__icontains=title) & Q(is_return=False)
            )
        else:
            queryset = queryset.filter(is_return=False)

        # 過濾超時的書籍，假設你有一個預計歸還日期的欄位
        # 這裡假設預計歸還日期欄位為 return_date
        current_time = timezone.now()
        queryset = queryset.filter(return_date__lt=current_time)

        for query in queryset:
            if query.fine_amount is None:
                query.fine_amount = query.book.price

        # transaction.atomic() 的主要目的是確保資料庫操作的原子性，即一個事務中的所有操作都要麼全部成功，要麼全部失敗。
        # 如果事務中的任何操作失敗，則所有的更改都將被回滾，資料庫將保持原狀。
                
        # 使用 bulk_update 一次性保存修改
        with transaction.atomic():
            BorrowingRecord.objects.bulk_update(queryset, ["fine_amount"])

        return queryset


class BookDetailView(DetailView):
    template_name = "book_detail.html"
    model = Book
    context_object_name = "detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book = self.get_object()
        context["book_logs"] = BorrowingRecord.objects.filter(book=book).order_by(
            "return_date"
        )[:10]

        return context


class BorrowerDetailView(DetailView):
    template_name = "borrower_detail.html"
    model = Borrower
    context_object_name = "detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()
        context["book_logs"] = BorrowingRecord.objects.filter(
            Q(borrower__id=user.id) & Q(is_return=False)
        ).order_by("return_date")

        context["amount"] = "{:.2f}".format(
            sum(
                [
                    amount.fine_amount
                    for amount in context["book_logs"]
                    if amount.fine_amount
                ]
            )
        )

        return context


class ReserveDetailView(DetailView):
    template_name = "reserve_detail.html"
    model = ReserveRecord
    context_object_name = "detail"


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("book-create")
    template_name = "book_create.html"


class BorrowerCreateView(CreateView):
    model = Borrower
    form_class = BorrowerForm
    success_url = reverse_lazy("book-list")
    template_name = "signup.html"


class ReserveCreateView(CreateView):
    model = ReserveRecord
    form_class = ReserveRecordForm
    success_url = reverse_lazy("book-list")
    template_name = "reserve_create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        borrower = self.request.user
        book = get_object_or_404(Book, id=self.kwargs["pk"])

        if book.quantity_in_stock > 0:
            messages.success(self.request, "預約成功！！")

            form.instance.borrower = borrower
            form.instance.book = book

            book.quantity_in_stock -= 1
            book.save()

            return super().form_valid(form)
        else:
            messages.error(self.request, "預約失敗！！ 書籍已全數借出！！")
            return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower'] = self.request.user
        context['book'] = get_object_or_404(Book, id=self.kwargs['pk'])

        return context
    

class ReserveRecordCreateView(CreateView):
    model = BorrowingRecord
    form_class = ReserveBorrowingRecordForm
    success_url = reverse_lazy("book-list")
    template_name = "reserve_record_create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_instance = form.save(commit=False)
        borrower = self.request.user
        book = get_object_or_404(Book, id=self.kwargs["book_pk"])

        form_instance.borrower = borrower
        form_instance.book = book
        form_instance.borrow_date = self.kwargs["date"]

        reserve_delete(self.request, self.kwargs["pk"])

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower'] = self.request.user
        context['book'] = get_object_or_404(Book, id=self.kwargs['book_pk'])
        context['date'] = self.kwargs['date']

        print("self.kwarg date:", self.kwargs["date"])

        return context
    

class RecordCreateView(CreateView):
    model = BorrowingRecord
    form_class = BorrowingRecordForm
    success_url = reverse_lazy("record-create")
    template_name = "record_create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_instance = form.save(commit=False)

        book_data = form.cleaned_data.get("book")

        if book_data.quantity_in_stock < 0:
            messages.error(self.request, "館內已無書籍儲藏！！")

            return self.form_invalid(form)
        else:
            book_data.quantity_in_stock -= 1
            book_data.save()

            form_instance.book = book_data
            form_instance.save()

        return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("book-list")
    template_name = "book_update.html"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        print(form.is_valid())
        return super().post(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_instance = form.save(commit=False)

        book_stock = form.cleaned_data.get("quantity_in_stock")
        book_stock += 1

        return super().form_valid(form)


class RecordUpdateView(UpdateView):
    model = BorrowingRecord
    form_class = BorrowingRecordForm
    template_name = "record_update.html"

    def get_success_url(self) -> str:
        record_obj = self.get_object()
        borrower_obj = record_obj.borrower
        return reverse_lazy("borrower-detail", kwargs={"pk": borrower_obj.pk})

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form_instance = form.save(commit=False)

        book_is_return = form.cleaned_data.get("is_return")

        if book_is_return:
            book_data = form.cleaned_data.get("book")

            book_data.quantity_in_stock += 1
            book_data.save()

            form_instance.book = book_data
            form_instance.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        record_obj = self.get_object()
        context["record"] = record_obj
        context["book"] = record_obj.book
        context["borrower"] = record_obj.borrower

        return context


class BorrowerUpdateView(UpdateView):
    model = Borrower
    form_class = BorrowerUpdateForm
    template_name = "borrower_update.html"

    def get_success_url(self) -> str:
        borrower_obj = self.get_object()
        return reverse_lazy("borrower-detail", kwargs={"pk": borrower_obj.pk})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()

        return redirect("book-list")

    context = {"book": book}

    return render(request, "book_delete.html", context)

def reserve_delete(request, pk, book_pk=None):
    reserve = get_object_or_404(ReserveRecord, pk=pk)

    if request.method == "POST":
        reserve.delete()

        if book_pk:
            book = get_object_or_404(Book, id=book_pk)
            book.quantity_in_stock += 1
            book.save()

        return redirect("reserve-list")
    
    context = {"reserve": reserve}
    
    return render(request, "reserve_delete.html", context)