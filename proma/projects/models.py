from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Project(TimeStampedModel):

    ACTIVE = 'ACTIVE'
    ARCHIVED = 'ARCHIVED'

    STATUS_CHOICES = (
        (ACTIVE, _('Active')),
        (ARCHIVED, _('Archived')),
    )

    FLAT_RATE = 'FLAT RATE'
    HOURLY_RATE = 'HOURLY RATE'
    DAILY_RATE = 'DAILY RATE'
    WEEKLY_RATE = 'WEEKLY RATE'
    MOUNTHLY_RATE = 'MOUNTHLY RATE'

    RATE_CHOICES = (
        (FLAT_RATE, _('Flat Rate')),
        (HOURLY_RATE, _('Hourly Rate')),
        (DAILY_RATE, _('Daily Rate')),
        (WEEKLY_RATE, _('Weekly Rate')),
        (MOUNTHLY_RATE, _('Mounthly Rate')),
    )

    USD = 'USD'
    EUR = 'EUR'
    PEN = 'PEN'

    CURRENCY_CHOICES = (
        (USD, 'USD'),
        (EUR, 'EUR'),
        (PEN, 'PEN'),
    )

    # TODO: get all currencies and put them in another file

    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)

    name = models.CharField(_('Name'), max_length=100)

    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    start_date = models.DateField(_('Start date'), default=timezone.now)
    end_date = models.DateField(_('End date'), blank=True, null=True)

    payment_type = models.CharField(
        _('Payment type'),
        max_length=20,
        choices=RATE_CHOICES,
        default=FLAT_RATE,
    )
    rate = models.DecimalField(_('Rate'), max_digits=10, decimal_places=2)
    currency = models.CharField(
        _('Currency'),
        max_length=5,
        choices=CURRENCY_CHOICES,
        default=USD,
    )
    notes = models.TextField(_('Notes'), blank=True, null=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        default_related_name = 'projects'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Expense(TimeStampedModel):

    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    name = models.CharField(_('Name'), max_length=100)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    date = models.DateField(_('Date'), default=timezone.now)

    notes = models.TextField(_('Notes'), blank=True, null=True)
    attachment = models.FileField(
        _('Attachment'),
        upload_to='projects/expense/attachment/%Y/%m/%d/',
        blank=True,
        null=True,
    )
    is_billable = models.BooleanField(_('Is billable?'), default=False)

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')
        default_related_name = 'expenses'
        ordering = ('name',)

    def __str__(self):
        return self.name
