from decimal import Decimal

from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext as _

from proma.common.forms import FormWithDateFields
from proma.invoices.models import Invoice

from .models import Expense, Project, Timesheet


class ProjectForm(FormWithDateFields, forms.ModelForm):

    date_fields = ("start_date", "end_date")

    def clean_end_date(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError(
                _("The end date must be greater than start date")
            )
        return end_date

    class Meta:
        model = Project
        fields = (
            "client",
            "name",
            "start_date",
            "end_date",
            "payment_type",
            "rate",
            "currency",
            "notes",
        )


class ExpenseForm(FormWithDateFields, forms.ModelForm):

    date_fields = ("date",)

    class Meta:
        model = Expense
        fields = (
            "name",
            "amount",
            "project",
            "date",
            "notes",
            "attachment",
            "is_billable",
        )


class CreateInvoiceFromProjectForm(forms.Form):

    description = forms.CharField(label=_("Description"), max_length=100)

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project

    def save(self, *args, **kwargs):
        raise NotImplementedError


class CreateInvoiceFlatForm(CreateInvoiceFromProjectForm):

    amount = forms.DecimalField(label=_("Amount"), validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        return Invoice.create_from_project_flat(
            self.project, self.cleaned_data["description"], self.cleaned_data["amount"]
        )


class CreateInvoiceRateForm(CreateInvoiceFromProjectForm):

    rate = forms.DecimalField(validators=[MinValueValidator(0)])
    units = forms.DecimalField(validators=[MinValueValidator(0)])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rate"].initial = self.project.rate
        self._set_labels()

    def save(self, *args, **kwargs):
        return Invoice.create_from_project_rate(
            self.project,
            self.cleaned_data["description"],
            self.cleaned_data["rate"],
            self.cleaned_data["units"],
        )

    def _set_labels(self):
        units_label = _("Units")
        rate_label = _("Rate")
        if self.project.payment_type == Project.HOURLY_RATE:
            rate_label = _("Per hour")
            units_label = _("Hours")
        elif self.project.payment_type == Project.DAILY_RATE:
            rate_label = _("Per day")
            units_label = _("Days")
        elif self.project.payment_type == Project.WEEKLY_RATE:
            rate_label = _("Per week")
            units_label = _("Weeks")
        elif self.project.payment_type == Project.MOUNTHLY_RATE:
            rate_label = _("Per month")
            units_label = _("Months")

        self.fields["rate"].label = rate_label
        self.fields["units"].label = units_label


class CreateInvoicePercentageForm(CreateInvoiceFromProjectForm):

    percentage = forms.IntegerField(
        label=_("Percentage"), validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def save(self, *args, **kwargs):
        amount = self.project.rate * (self.cleaned_data["percentage"] / Decimal(100))
        return Invoice.create_from_project_flat(
            self.project, self.cleaned_data["description"], amount
        )


class TimesheetForm(FormWithDateFields, forms.ModelForm):

    date_fields = ("date_start", "date_end")

    class Meta:
        model = Timesheet
        fields = ("label", "project", "date_start", "date_end")
