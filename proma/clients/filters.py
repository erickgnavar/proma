import django_filters

from proma.common.helpers import CommonFilterHelper

from .models import Client


class ClientFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    alias = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Client
        fields = (
            'status', 'alias', 'name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = CommonFilterHelper()
