from babel.dates import format_timedelta
from django.db import models
from django.utils import timezone
from django.utils.translation import get_language, get_language_info
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from . import exceptions


class Project(TimeStampedModel):

    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"

    STATUS_CHOICES = ((ACTIVE, _("Active")), (ARCHIVED, _("Archived")))

    FLAT_RATE = "FLAT RATE"
    HOURLY_RATE = "HOURLY RATE"
    DAILY_RATE = "DAILY RATE"
    WEEKLY_RATE = "WEEKLY RATE"
    MOUNTHLY_RATE = "MOUNTHLY RATE"

    RATE_CHOICES = (
        (FLAT_RATE, _("Flat Rate")),
        (HOURLY_RATE, _("Hourly Rate")),
        (DAILY_RATE, _("Daily Rate")),
        (WEEKLY_RATE, _("Weekly Rate")),
        (MOUNTHLY_RATE, _("Mounthly Rate")),
    )

    USD = "USD"
    EUR = "EUR"
    PEN = "PEN"

    CURRENCY_CHOICES = ((USD, "USD"), (EUR, "EUR"), (PEN, "PEN"))

    # TODO: get all currencies and put them in another file

    client = models.ForeignKey("clients.Client", on_delete=models.CASCADE)

    name = models.CharField(_("Name"), max_length=100)

    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default=ACTIVE
    )

    start_date = models.DateField(_("Start date"), default=timezone.now)
    end_date = models.DateField(_("End date"), blank=True, null=True)

    payment_type = models.CharField(
        _("Payment type"), max_length=20, choices=RATE_CHOICES, default=FLAT_RATE
    )
    rate = models.DecimalField(_("Rate"), max_digits=10, decimal_places=2)
    currency = models.CharField(
        _("Currency"), max_length=5, choices=CURRENCY_CHOICES, default=USD
    )
    notes = models.TextField(_("Notes"), blank=True, null=True)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        default_related_name = "projects"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Expense(TimeStampedModel):

    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    name = models.CharField(_("Name"), max_length=100)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    date = models.DateField(_("Date"), default=timezone.now)

    notes = models.TextField(_("Notes"), blank=True, null=True)
    attachment = models.FileField(
        _("Attachment"),
        upload_to="projects/expense/attachment/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    is_billable = models.BooleanField(_("Is billable?"), default=False)

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")
        default_related_name = "expenses"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Timesheet(TimeStampedModel):

    project = models.ForeignKey(
        "projects.Project", on_delete=models.SET_NULL, null=True, blank=True
    )

    is_active = models.BooleanField(_("Is active?"), default=False)
    label = models.CharField(_("Label"), max_length=50, null=True, blank=True)
    date_start = models.DateTimeField(_("Date start"), default=timezone.now)
    date_end = models.DateTimeField(_("Date end"), null=True, blank=True)

    class Meta:
        verbose_name = _("Timesheet")
        verbose_name_plural = _("Timesheets")
        default_related_name = "timesheets"
        ordering = ("-created",)

    def __str__(self):
        return self.label

    @property
    def diff(self):
        if self.date_end:
            return self.date_end - self.date_start
        return None

    @property
    def diff_humanize(self):
        if self.diff:
            # get_language return a format like en-us and this isn't allowed by babel
            lang = get_language_info(get_language())
            return format_timedelta(self.diff, format="long", locale=lang["code"])
        else:
            return ""

    def finish(self):
        self.date_end = timezone.now()
        self.is_active = False
        self.save()

    @classmethod
    def clock_in(cls, project=None, label=None):
        if cls.objects.filter(is_active=True).exists():
            raise exceptions.ActiveTimesheetExists

        return cls.objects.create(project=project, is_active=True, label=label)

    @classmethod
    def clock_out(cls):
        timesheet = cls.objects.filter(is_active=True).first()
        if timesheet is None:
            raise exceptions.ActiveTimesheetDoesNotExist
        timesheet.finish()
