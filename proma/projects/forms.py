from django import forms
from django.utils.translation import ugettext as _

from proma.common.forms import FormWithDateFields

from .models import Expense, Project


class ProjectForm(FormWithDateFields, forms.ModelForm):

    date_fields = ('start_date', 'end_date',)

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError(_('The end date must be greater than start date'))
        return end_date

    class Meta:
        model = Project
        fields = (
            'client', 'name', 'start_date', 'end_date',
            'payment_type', 'rate', 'currency', 'notes',
        )


class ExpenseForm(FormWithDateFields, forms.ModelForm):

    date_fields = ('date',)

    class Meta:
        model = Expense
        fields = (
            'name', 'amount', 'project', 'date',
            'notes', 'attachment',
        )
