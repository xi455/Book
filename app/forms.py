from django import forms

from app.models import Book, Borrower, BorrowingRecord


class BookForm(forms.ModelForm):
    published_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"},
            format="%Y-%m-%d",
        ),
    )

    class Meta:
        model = Book
        fields = "__all__"


class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ["username", "first_name", "phone_number", "address"]


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


# class BorrowingRecordUpdateForm(forms.ModelForm):
#     class Meta:
#         model = BorrowingRecord
#         fields = ['fine_amount', 'is_return']
