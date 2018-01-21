from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Client(TimeStampedModel):

    ACTIVE = 'ACTIVE'
    ARCHIVED = 'ARCHIVED'

    STATUS_CHOICES = (
        (ACTIVE, _('Active')),
        (ARCHIVED, _('Archived')),
    )

    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'), max_length=255)
    tax_identifier = models.CharField(_('Tax identifier'), max_length=20, blank=True, null=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        default_related_name = 'clients'
        ordering = ('name',)

    def __str__(self):
        return self.name
