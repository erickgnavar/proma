import django_filters

from proma.common.helpers import CommonFilterHelper

from .models import Invoice


class InvoiceFilter(django_filters.FilterSet):

    number = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Invoice
        fields = ("status", "client", "project", "number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = CommonFilterHelper()
