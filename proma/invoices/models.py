import secrets
from decimal import Decimal
from functools import reduce

from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from .exceptions import InvoiceException
from .querysets import InvoiceQuerySet


def default_due_date():
    return timezone.now() + relativedelta(months=1)


class Invoice(TimeStampedModel):

    DRAFT = 'DRAFT'
    OPEN = 'OPEN'
    PAID = 'PAID'
    CANCELLED = 'CANCELLED'

    STATUS_CHOICES = (
        (DRAFT, _('Draft')),
        (OPEN, _('Open')),
        (PAID, _('Paid')),
        (CANCELLED, _('Cancelled')),
    )

    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)

    number = models.CharField(_('Number'), max_length=64, unique=True, default=secrets.token_hex, editable=False)
    # use a random value intil the invoice is active
    issue_date = models.DateField(_('Issue date'), default=timezone.now)
    due_date = models.DateField(_('Due date'), default=default_due_date)

    opening_date = models.DateField(_('Opening date'), null=True, editable=False)
    payment_date = models.DateField(_('Payment date'), null=True, editable=False)
    cancellation_date = models.DateField(_('Cancellation date'), null=True, editable=False)

    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
    )

    tax_percent = models.DecimalField(
        _('Tax %'),
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal(0)),
            MaxValueValidator(Decimal(100)),
        ],
        null=True,
        blank=True,
    )
    tax_total = models.DecimalField(_('Tax total'), max_digits=10, decimal_places=2, default=0, editable=False)
    subtotal = models.DecimalField(_('Subtotal'), max_digits=10, decimal_places=2, default=0, editable=False)
    total = models.DecimalField(_('Total'), max_digits=10, decimal_places=2, default=0, editable=False)

    attachment = models.FileField(
        _('Attachment'),
        upload_to='invoices/invoice/attachment/%Y/%m/%d/',
        blank=True,
        null=True,
    )

    notes = models.TextField(_('Notes'), blank=True, null=True)

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        default_related_name = 'invoices'
        ordering = ('number',)

    def __str__(self):
        if self.status == self.DRAFT:
            return str(_('Draft'))
        else:
            return f'#{self.number}'

    def open(self):
        if self.status != self.DRAFT:
            raise InvoiceException('Invalid status')
        if not self.items.count():
            raise InvoiceException('The invoice must has at least 1 item to be opened')
        self.opening_date = timezone.now()
        self.status = self.OPEN
        self._compute_number()

    def pay(self):
        if self.status != self.OPEN:
            raise InvoiceException('Invalid status')
        self.payment_date = timezone.now()
        self.status = self.PAID

    def cancel(self):
        if self.status != self.OPEN:
            raise InvoiceException('Invalid status')
        self.cancellation_date = timezone.now()
        self.status = self.CANCELLED

    @property
    def can_be_edited(self):
        return self.status == self.DRAFT

    def _compute_number(self):
        if self.status == self.DRAFT:
            return
        self.number = self.compute_next_number()

    @classmethod
    def compute_next_number(cls):
        """
        Compute invoice number using the current year and a counter based
        in the number of invoices created
        """
        now = timezone.now()
        counter = cls.objects.exclude(status=cls.DRAFT).filter(
            issue_date__year__gte=now.year,
            issue_date__year__lte=now.year + 1,
        ).count() + 1
        # TODO: Add more tests for this method
        return f'{now.year}{str(counter).zfill(5)}'

    def compute_amounts(self):
        self.subtotal = reduce(lambda acc, item: acc + item.total, self.items.all(), Decimal(0))
        if self.tax_percent is None:
            self.tax_total = Decimal(0)
        else:
            self.tax_total = self.subtotal * (self.tax_percent / Decimal(100))
        self.total = self.subtotal + self.tax_total


class Item(TimeStampedModel):

    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)

    description = models.CharField(_('Description'), max_length=100)
    units = models.DecimalField(_('Units'), max_digits=10, decimal_places=2)
    rate = models.DecimalField(_('Rate'), max_digits=10, decimal_places=2)
    total = models.DecimalField(_('Total'), max_digits=10, decimal_places=2, default=0, editable=False)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Item')
        default_related_name = 'items'

    def __str__(self):
        return f'{self.description}: {self.total}'

    def save(self, *args, **kwargs):
        self._compute_total()
        return super().save(*args, **kwargs)

    def _compute_total(self):
        self.total = self.rate * self.units
