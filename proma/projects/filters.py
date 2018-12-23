import django_filters

from proma.common.helpers import CommonFilterHelper

from .models import Expense, Project, Timesheet


class ProjectFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Project
        fields = ("status", "client", "name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = CommonFilterHelper()


class ExpenseFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Expense
        fields = ("project", "is_billable", "name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = CommonFilterHelper()


class TimesheetFilter(django_filters.FilterSet):

    label = django_filters.CharFilter(lookup_expr="icontains")
    date_start = django_filters.CharFilter(lookup_expr="gte")
    date_end = django_filters.CharFilter(lookup_expr="lte")

    class Meta:
        model = Timesheet
        fields = ("project", "label", "date_start", "date_end")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = CommonFilterHelper()
        self.form.fields["date_start"].widget.attrs["data-provide"] = "datepicker"
        self.form.fields["date_start"].widget.attrs["data-date-format"] = "yyyy-mm-dd"
        self.form.fields["date_end"].widget.attrs["data-provide"] = "datepicker"
        self.form.fields["date_end"].widget.attrs["data-date-format"] = "yyyy-mm-dd"
