from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.models import Book, Borrower, ReserveRecord, BorrowingRecord


class BookForm(forms.ModelForm):
    published_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
    )
    admission_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
    )

    class Meta:
        model = Book
        fields = "__all__"


class BorrowerForm(UserCreationForm):
    class Meta:
        model = Borrower
        fields = ["username", "first_name", "phone_number", "address"]


class BorrowerUpdateForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ["first_name", "phone_number", "address"]


class BorrowingRecordForm(forms.ModelForm):
    borrow_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
    )
    return_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
    )
    actual_return_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
        required=False,
    )

    class Meta:
        model = BorrowingRecord
        fields = "__all__"


class BorrowingRecordUpdateForm(forms.ModelForm):
    borrow_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
    )
    return_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
    )
    actual_return_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
        required=True,
    )

    class Meta:
        model = BorrowingRecord
        fields = "__all__"


class ReserveRecordForm(forms.ModelForm):

    reserve_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
    )

    class Meta:
        model = ReserveRecord
        fields = ["reserve_date"]
        exclude = ["borrower", "book"]


class ReserveBorrowingRecordForm(forms.ModelForm):
    borrow_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
        required=False,
    )
    return_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
    )
    actual_return_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
        required=False,
    )

    class Meta:
        model = BorrowingRecord
        exclude = ["book", "borrower", "borrow_date"]
