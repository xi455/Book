from typing import Any

from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from app.forms import BookForm, BorrowerForm, BorrowingRecordForm
from app.models import Book, Borrower, BorrowingRecord

# Create your views here.


class BookListItem(ListView):
    template_name = "book_list.html"
    model = Book
    context_object_name = "items"
    paginate_by = 10
    # ordering = "-published_date"

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("book_title")

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset


class BorrowerListItem(ListView):
    template_name = "borrower_list.html"
    model = Borrower
    context_object_name = "items"
    paginate_by = 10
    # ordering = "-published_date"

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

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("book_title")

        if title:
            queryset = queryset.filter(
                Q(book__title__icontains=title) & Q(is_return=False)
            )

        queryset = queryset.filter(is_return=False)

        return queryset


class BookDetailView(DetailView):
    template_name = "book_detail.html"
    model = Book
    context_object_name = "detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book = self.get_object()
        context["book_logs"] = BorrowingRecord.objects.filter(book=book)[:10]

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


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("book-create")
    template_name = "book_create.html"


class RecordCreateView(CreateView):
    model = BorrowingRecord
    form_class = BorrowingRecordForm
    success_url = reverse_lazy("record-create")
    template_name = "record_create.html"


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("book-list")
    template_name = "book_update.html"


class RecordUpdateView(UpdateView):
    model = BorrowingRecord
    form_class = BorrowingRecordForm
    template_name = "record_update.html"

    def get_success_url(self) -> str:
        record_obj = self.get_object()
        borrower_obj = record_obj.borrower
        return reverse_lazy("borrower-detail", kwargs={"pk": borrower_obj.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        record_obj = self.get_object()
        context["record"] = record_obj
        context["book"] = record_obj.book
        context["borrower"] = record_obj.borrower

        return context


class BorrowerUpdateView(UpdateView):
    model = Borrower
    form_class = BorrowerForm
    template_name = "borrower_update.html"

    def get_success_url(self) -> str:
        borrower_obj = self.get_object()
        return reverse_lazy("borrower-detail", kwargs={"pk": borrower_obj.pk})


class BookNewRecommendListItem(ListView):
    template_name = "book_new_recommend.html"
    model = Book
    context_object_name = "items"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get("book_title")

        if title:
            queryset = queryset.filter(book__title__icontains=title)

        return queryset


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()

        return redirect("book-list")

    context = {"book": book}

    return render(request, "book_delete.html", context)