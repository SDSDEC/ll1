from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.
from .models import BookInstance

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

    class Meta:
        model = BookInstance
        fields = ['due_back', ]
        labels = {'due_back': _('Renewal date'), }
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).'), }

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'summary', 'isbn', 'genre']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        labels = {
            'title': 'Title',
            'summary': 'Summary',
            # и т.д.
        }

        help_texts = {
            'isbn': '13 Character ISBN number',
        }

class BookDeleteForm(forms.Form):
    confirmation = forms.BooleanField(
        required=True,
        widget=forms.HiddenInput(),
        initial=True
    )