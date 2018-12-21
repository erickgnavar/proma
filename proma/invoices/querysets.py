from django.db import models


class InvoiceQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(status="PAID")

    def open(self):
        return self.filter(status="OPEN")

    def cancelled(self):
        return self.filter(status="CANCELLED")

    def non_draft(self):
        return self.exclude(status="DRAFT")
