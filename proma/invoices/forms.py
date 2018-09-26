from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext as _

from proma.common.forms import FormWithDateFields

from .models import Invoice, Item


class InvoiceForm(FormWithDateFields, forms.ModelForm):

    date_fields = ('issue_date', 'due_date')

    def clean_due_date(self):
        issue_date = self.cleaned_data.get('issue_date')
        due_date = self.cleaned_data.get('due_date')
        if issue_date and due_date:
            if issue_date >= due_date:
                raise forms.ValidationError(_('Due date must be greater than issue date'))
        return due_date

    class Meta:
        model = Invoice
        fields = (
            'client', 'project',
            'issue_date', 'due_date',
            'tax_percent', 'notes', 'attachment',
        )


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = (
            'description', 'units', 'rate',
        )


ItemsFormset = inlineformset_factory(Invoice, Item, ItemForm, extra=0)


class PayInvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = (
            'payment_notes',
        )
        widgets = {
            'payment_notes': forms.Textarea(attrs={
                'cols': 30,
                'rows': 3,
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_notes'].required = True
