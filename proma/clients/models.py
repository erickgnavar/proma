from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


class Client(TimeStampedModel):

    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"

    STATUS_CHOICES = ((ACTIVE, _("Active")), (ARCHIVED, _("Archived")))

    name = models.CharField(
        _("Legal name"),
        max_length=100,
        help_text=_("This name will be used for invoicing"),
    )
    email = models.EmailField(_("Email"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=20, null=True, blank=True)
    tax_identifier = models.CharField(
        _("Tax identifier"), max_length=20, blank=True, null=True
    )
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default=ACTIVE
    )
    alias = models.CharField(_("Alias"), max_length=30)
    address = models.CharField(_("Address"), max_length=255, null=True, blank=True)
    state = models.CharField(_("State"), max_length=100, null=True, blank=True)
    city = models.CharField(_("City"), max_length=100, null=True, blank=True)
    country = models.CharField(_("Country"), max_length=100, null=True, blank=True)
    zipcode = models.CharField(_("Zipcode"), max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        default_related_name = "clients"
        ordering = ("name",)

    def __str__(self):
        return self.alias or self.name
