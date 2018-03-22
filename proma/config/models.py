import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Configuration(TimeStampedModel):

    company_logo = models.ImageField(
        _('Logo'),
        upload_to='config/configuration/',
        help_text=_('size should be 250pt x 100pt'),
        null=True,
        blank=True,
    )
    company_legal_name = models.CharField(_('Legal name'), max_length=255, null=True, blank=True)
    company_email = models.EmailField(_('Email'), max_length=255, null=True, blank=True)
    company_phone = models.CharField(_('Phone'), max_length=20, null=True, blank=True)
    company_tax_identifier = models.CharField(_('Tax identifier'), max_length=20, null=True, blank=True)
    company_address = models.CharField(_('Address'), max_length=255, null=True, blank=True)
    company_state = models.CharField(_('State'), max_length=100, null=True, blank=True)
    company_city = models.CharField(_('City'), max_length=100, null=True, blank=True)
    company_country = models.CharField(_('Country'), max_length=100, null=True, blank=True)
    company_zipcode = models.CharField(_('Zipcode'), max_length=10, null=True, blank=True)

    def str(self):
        return 'config'

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create()
        return instance

    def get_info(self, prefix):
        res = {}
        for field in self._meta.get_fields():
            if field.name.startswith(prefix):
                res[field.name.replace(f'{prefix}_', '')] = getattr(self, field.name)
        return res

    def get_company_logo_path(self):
        if self.company_logo:
            return os.path.join(settings.MEDIA_ROOT, self.company_logo.name)
        return None
