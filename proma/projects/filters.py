import django_filters

from proma.common.helpers import CommonFilterHelper

from .models import Expense, Project


class ProjectFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = (
            'status', 'client', 'name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = CommonFilterHelper()


class ExpenseFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Expense
        fields = (
            'project', 'is_billable', 'name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = CommonFilterHelper()
